import numpy as np

# Fi   -> F(i+1) (masflo)
# Hi   -> H(i+1) (HM)
# WIJi -> WIJ(i+1) (dcross)
# Pi   -> P(i+1) (aximom)

class variables:

   ALPHA   = 90 # (ANGLE )
   AXLN    = 0.1
   DELTA   = 0.5
   FACK    = 0.01
   FT      = 0.1 # turbulent factor used to compensate imperfect analogy bw turbulent transport of enthalpy and momentum
   GAMA    = 0.5
   GC      = 9.81 # g
   NCHANL  = 14 # no of subchannel
   NK      = 19 # no of connections
   NNODE   = 100
   RDIA    = 0.01308  
   RHO     = 817.4  
   SLP     = 0.5 
   THETA   = 0.5 # IMPLICIT FAV
   VISC    = 0.000011
   DELX    = AXLN/(NNODE-1)
   PIN     = 12262500

   GAP     = [.0018034,.0009,.0009,.0018034,.0018034,.0009,.0018034,.0009,.0018034,.004140000,.00414,.0018034,.000991,.0019558,.0019558,.000991,.00194,.00194,.00194]
   #Hydraulic Diameter
   HDIA    = [.0056277,.0056277,.0084154,.005627,.0084154,.0084154,.0074985,.0094202,.0074485,.0084154,.0070309,.0070309,.0070309,.0070309]
   #Heat Generation per unit volume  might be kw/m^2
   HF      = [607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59]
   #Heated Perimeter
   HPERI   = [.010272,.010272,.020546,.020546,.020546,.020546,.020546,.020546,.020546,.020546,.020371,.040742,.040742,.020371]
   # representation of interconnections of different subchannels IC -- slef , JC -- adjacent
   IC      = [1, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 9, 6, 7, 9, 10, 11, 12, 13] 
   JC      = [2, 3, 5, 4, 5, 6, 8, 10, 7, 8, 9, 10, 11, 12, 13, 14, 12, 13, 14]
   #A -Area -- constant
   A       = [.000014451,.000014451,.000043225,.000028903,.000043225,.000043225,.000038516000,.000048387,.000038516,.000043225,.000035806,.000071612,.000071612,.000035806]
            
   def initializer(self):
      
      # Matrix B -- used in XB sub rooutine, B0 and B1 support variables in XB
      self.B       = np.zeros(self.NCHANL)
      self.B1      = np.zeros(self.NCHANL)
      self.B2      = np.zeros(self.NCHANL)
      
      #Used in HM -- c1,c2.c3
      self.C1      = np.zeros(self.NCHANL)
      self.C2      = np.zeros(self.NCHANL)
      self.C3      = np.zeros(self.NCHANL)
      #rotine xd -- cij0, cij1
      self.CIJ0    = [0] * self.NK
      self.CIJ1    = [0] * self.NK
      
      #Matrix D -- calculated by XD
      self.D       = np.zeros(self.NK)
      #Matrix DELH -- enthalpy diff between 2 adjacent subchannel
      self.DELH    = np.zeros(self.NK)
      
      #General Purpose use -- size NK
      self.ERR     = np.zeros(self.NK)
      self.ERROR   = np.zeros(self.NK)

      #F0 -- initial mass flow rate for 14 subchannels, F1 --final mass flow rate for 14 subchannels, temp variable for copying F11 
      self.F0      = [.090576301,.090576301,.331301059,.1810780788,.331301059,.331301059,.27866318100,.39238281,.278663181,.331301059,.250849063,.501698126,.501698126,.25084906] 
      self.F1      = [0] * self.NCHANL  
      self.F11     = np.zeros(self.NK)
      
        
      #H0 - initial enthalpy of sub-channels,, H1 -final enthalpy of sub-channels,
      self.H0      = [1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7000,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7000,1100.7,1100.7,1100.7]
      self.H1      = np.zeros(self.NK)

      #Cross Flow enthalpy -- calculated in HM
      self.HSTAR   = np.zeros(self.NK)
      
      
      '''P0 -- initial press, P1 -- outlet pressure, P11 -- temp var for copying P1
      PB - used in main file for calculating source of gauss sub routine
      PM0 -- used in main file can be removed 
      '''      
      self.P0      = np.zeros(self.NK)
      self.P1      = np.zeros(self.NK)
      self.P11     = np.zeros(self.NK)
      self.PB      = np.zeros(self.NK)
      self.PM0     = np.zeros(self.NK)
      
      #Heat generation inside the channel
      self.Q       = np.zeros(self.NCHANL)
      
      #Reynold number
      self.RE      = [0] *self.NK
      
      #S -- connecting matrix , calculated by SKI, ST -- transpose of S calculated by SKI
      #temp vars
      self.S       = np.zeros((self.NK, self.NK))
      self.S5      = np.zeros((self.NK, self.NK))
      #defn moved in XB --  self.SAVE    = np.zeros(self.NK)
      self.SD      = np.zeros((self.NK, self.NK))
      self.SS      = np.zeros(self.NCHANL)
      self.ST      = [[0.0] * self.NK for _ in range(self.NK)]  

      #USTAR0 -- initial velocity, USTAR1 -- final velocity, USTAR D1 -- temp VAR for USTD1 
      self.USTAR0  = [0.0] * self.NK
      self.USTAR1  = [0.0] * self.NK
      self.USTD1   = [0] * self.NK
      
      #all used in D corss
      self.W2      = np.zeros(self.NK)
      self.WIJ0    = [0] * self.NK
      self.WIJ1    = [0] * self.NK
      self.WIJIN   = 0.0
      #used in wprim routine
      self.WPR     = np.zeros(self.NK)
      
      '''
      XA -- matrix a
      XDELH -- Sub-routine HM
      XH, XHS, XHST -- subroutine HM
      XM,XM0,XMI -- used in main for calculation M in main
      XMLT -- used in calculation of S, ST*Ustar1
      XUST0,XUST1 -- used in star sub-routine
      
      '''
      self.XA      = np.zeros(self.NCHANL)
      self.XDELH   = np.zeros((self.NK, self.NK))
      self.XH      = np.zeros((self.NCHANL, self.NCHANL))
      self.XHS     = np.zeros((self.NK, self.NK))
      self.XHST    = np.zeros((self.NK, self.NK))
      self.XM      = np.zeros((self.NK, self.NK))
      self.XM0     = np.zeros((self.NK, self.NK))
      self.XMI     = np.zeros((self.NK, self.NK))
      self.XMLT    = np.zeros((self.NK, self.NK))
      self.XUST0   = [[0.0] * self.NK for _ in range(self.NK)]
      self.XUST1   = [[0.0] * self.NK for _ in range(self.NK)]
      self.XUSTD1  = np.zeros((self.NK, self.NK))
      # matrix calculation for ft*stranspose*delu*wpr/area
      self.XY      = [0.0] * self.NCHANL
      #used in wprim routine 
      self.XZ      = [0.0] * self.NK
      
      #used in AXIMOM
      self.YU1     = np.zeros((self.NK, self.NK))

