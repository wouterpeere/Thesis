import numpy as np
import pygfunction as gt
from scipy import pi

def main():

    #loads
    qh = -443.9*1000
    qm = -146.4*1000
    qa = -59.0*1000

    # -------------------------------------------------------------------------
    # Simulation parameters
    # -------------------------------------------------------------------------

    # Borehole dimensions
    D = 4.0             # Borehole buried depth (m)
    H = 100.           # Borehole length (m)
    r_b = 0.075         # Borehole radius (m)
    B = 6.5             # Borehole spacing (m)

    # Pipe dimensions
    rp_out = 0.0167     # Pipe outer radius (m)
    rp_in = 0.013      # Pipe inner radius (m)
    D_s = 0.062         # Shank spacing (m)
    epsilon = 1.0e-6    # Pipe roughness (m)

    # Pipe positions
    # Single U-tube [(x_in, y_in), (x_out, y_out)]
    pos_pipes = [(-D_s, 0.), (D_s, 0.)]

    # Ground properties
    alpha = 0.075/24/3600      # Ground thermal diffusivity (m2/s)
    k_s = 1.8           # Ground thermal conductivity (W/m.K)

    # Grout properties
    k_g = 1.0           # Grout thermal conductivity (W/m.K)

    # Pipe properties
    k_p = 0.4           # Pipe thermal conductivity (W/m.K)

    # Fluid properties
    m_flow = 0.043*443.9       # Total fluid mass flow rate per borehole (kg/s)
    cp_f = 4000.        # Fluid specific isobaric heat capacity (J/kg.K)
    den_f = 1016.       # Fluid density (kg/m3)
    visc_f = 0.00179    # Fluid dynamic viscosity (kg/m.s)
    k_f = 0.513         # Fluid thermal conductivity (W/m.K)

    # Number of segments per borehole
    nSegments = 12
    ty = 87600*3600.
    tm = 744*3600.
    td = 6*3600.
    time = np.array([td,td+tm,ty+tm+td])

    # -------------------------------------------------------------------------
    # Borehole field
    # -------------------------------------------------------------------------
    N_1 = 2
    N_2 = 5

    qa = qa / 120 * 19
    qm = qm / 120 * 19
    qh = qh / 120 * 19

    m_flow = -qh*.043/1000

    for loop in range(5):
        # Field of 6x4 (n=24) boreholes

        boreField = gt.boreholes.rectangle_field(N_1, N_2, B, B, H, D, r_b)
        #boreField = gt.boreholes.U_shaped_field(10,10,B,B,H,D,r_b)
        boreField = gt.boreholes.L_shaped_field(10,10,B,B,H,D,r_b)



        # -------------------------------------------------------------------------
        # Initialize pipe model
        # -------------------------------------------------------------------------

        # Pipe thermal resistance
        R_p = gt.pipes.conduction_thermal_resistance_circular_pipe(rp_in,
                                                                   rp_out,
                                                                   k_p)
        # Fluid to inner pipe wall thermal resistance (Single U-tube)
        h_f = gt.pipes.convective_heat_transfer_coefficient_circular_pipe(m_flow,
                                                                          rp_in,
                                                                          visc_f,
                                                                          den_f,
                                                                          k_f,
                                                                          cp_f,
                                                                          epsilon)
        R_f = 1.0/(h_f*2*pi*rp_in)

        # Single U-tube, same for all boreholes in the bore field
        UTubes = []
        for borehole in boreField:
            SingleUTube = gt.pipes.SingleUTube(pos_pipes, rp_in, rp_out,
                                               borehole, k_s, k_g, R_f + R_p)
            UTubes.append(SingleUTube)
        # Calculate the g-function for uniform borehole wall temperature
        gfunc_uniform_T = gt.gfunction.uniform_temperature(
                boreField, time, alpha, nSegments=nSegments, disp=False)

        Ra = (gfunc_uniform_T[2]-gfunc_uniform_T[1])/(2*pi*k_s)
        Rm = (gfunc_uniform_T[1]-gfunc_uniform_T[0])/(2*pi*k_s)
        Rd = (gfunc_uniform_T[0])/(2*pi*k_s)

        #print "G_funct",gfunc_uniform_T[2]
        print 'Ra',Ra
        print "Rm",Rm
        print "Rd",Rd
        Rb = 0.2 #m.K/W
        #Tm = UTubes[0].get_outlet_temperature(0.0,,m_flow,cp_f)
        Tg = 18 #C

        L = -(qa*Ra + qm*Rm + qh*Rd +qh*Rb)/(Tg-(0+qh/cp_f/m_flow)/2)

        H = L/(len(boreField))
        print "L = ", L, " H=",H, len(boreField)
# Main function
if __name__ == '__main__':
    main()