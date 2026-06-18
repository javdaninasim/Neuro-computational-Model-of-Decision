'''

Integration circuit from:

Wang, X.-J. Probabilistic decision making by slow reverberation in cortical circuits. Neuron, 2002, 36, 955-968.

@author: Klaus Wimmer and Albert Compte

wimmer.klaus@googlemail.com
acompte@clinic.ub.es

'''

from brian2 import *
import numpy
from scipy.io import savemat


def make_integration_circuit():

    '''
    Creates the spiking network described in Wang 2002.

    returns:
        groups, connections, update_nmda, subgroups

    groups, connections, and update_nmda have to be added to the "Network" in order to run the simulation.
    subgroups is used for establishing connections between the sensory and integration circuit; do not add subgroups to the "Network"

    '''

    # -----------------------------------------------------------------------------------------------
    # Model parameters for the integration circuit
    # -----------------------------------------------------------------------------------------------

    # Populations
    f_E = 0.15                                   # Fraction of stimulus-selective excitatory neurons
    N = 2000                                     # Total number of neurons
    f_inh = 0.2                                  # Fraction of inhibitory neurons
    NE = int(N * (1.0 - f_inh))                  # Number of excitatory neurons (1600)
    NI = int(N * f_inh)                          # Number of inhibitory neurons (400)
    N_D1 = int(f_E * NE)                         # Size of excitatory population D1
    N_D2 = N_D1                                  # Size of excitatory population D2
    N_DN = int((1.0 - 2.0 * f_E) * NE)           # Size of excitatory population DN

    # Connectivity - local recurrent connections
    w_p = 1.65                                 # Relative recurrent synaptic strength within populations D1 and D2 1.65
    w_m = 1.0 - f_E * (w_p - 1.0) / (1.0 - f_E)	# Relative recurrent synaptic strength of connections across populations D1 and D2 and from DN to D1 and D2
    gEE_AMPA = 0.05 * nS		                 # Weight of AMPA synapses between excitatory neurons
    gEE_NMDA = 0.165 * nS                        # Weight of NMDA synapses between excitatory neurons
    gEI_AMPA = 0.04 * nS                         # Weight of excitatory to inhibitory synapses (AMPA)
    gEI_NMDA = 0.13 * nS                         # Weight of excitatory to inhibitory synapses (NMDA)
    gIE_GABA = 1.3 * nS                          # Weight of inhibitory to excitatory synapses
    gII_GABA = 1.0 * nS                          # Weight of inhibitory to inhibitory synapses
    d = 0.5 * ms                                 # Transmission delay of recurrent excitatory and inhibitory connections

    # Connectivity - external connections
    gextE = 2.1 * nS                             # Weight of external input to excitatory neurons
    gextI = 1.63 * nS                            # Weight of external input to inhibitory neurons

    # Neuron model
    CmE = 0.5 * nF                               # Membrane capacitance of excitatory neurons
    CmI = 0.2 * nF                               # Membrane capacitance of inhibitory neurons
    gLeakE = 25.0 * nS                           # Leak conductance of excitatory neurons
    gLeakI = 20.0 * nS                           # Leak conductance of inhibitory neurons
    Vl = -70.0 * mV                              # Resting potential
    Vt = -50.0 * mV                              # Spiking threshold
    Vr = -55.0 * mV                              # Reset potential
    tau_refE = 2.0 * ms                          # Absolute refractory period of excitatory neurons
    tau_refI = 1.0 * ms                          # Absolute refractory period of inhibitory neurons

    # Synapse model
    VrevE = 0 * mV                               # Reversal potential of excitatory synapses
    VrevI = -70 * mV                             # Reversal potential of inhibitory synapses
    tau_AMPA = 2.0 * ms                          # Decay constant of AMPA-type conductances
    tau_GABA = 5.0 * ms                          # Decay constant of GABA-type conductances
    tau_NMDA_decay = 100.0 * ms                  # Decay constant of NMDA-type conductances
    tau_NMDA_rise = 2.0 * ms                     # Rise constant of NMDA-type conductances
    alpha_NMDA = 0.5 * kHz                       # Saturation constant of NMDA-type conductances

    # Inputs
    nu_ext_1 = 2392 * Hz				                 # Firing rate of external Poisson input to neurons in population D1
    nu_ext_2 = 2392 * Hz				                 # Firing rate of external Poisson input to neurons in population D2
    nu_ext = 2400 * Hz				                   # Firing rate of external Poisson input to neurons in population Dn and I


    # -----------------------------------------------------------------------------------------------
    # Set up the model
    # -----------------------------------------------------------------------------------------------

    # Neuron equations
    eqsE = '''
    dV/dt = (-gea*(V-VrevE) - gen*(V-VrevE)/(1.0+exp(-V/mV*0.062)/3.57) - gi*(V-VrevI) - (V-Vl)) / (tau): volt
    dgea/dt = -gea/(tau_AMPA) : 1
    dgi/dt = -gi/(tau_GABA) : 1
    dspre/dt = -spre/(tau_NMDA_decay)+alpha_NMDA*xpre*(1-spre) : 1
    dxpre/dt= -xpre/(tau_NMDA_rise) : 1
    gen : 1
    tau : second
    '''
    eqsI = '''
    dV/dt = (-gea*(V-VrevE) - gen*(V-VrevE)/(1.0+exp(-V/mV*0.062)/3.57) - gi*(V-VrevI) - (V-Vl)) / (tau): volt
    dgea/dt = -gea/(tau_AMPA) : 1
    dgi/dt = -gi/(tau_GABA) : 1
    gen : 1
    tau : second
    '''

    # Set up the integration circuit
    decisionE = NeuronGroup(NE, model=eqsE, threshold=Vt, reset=Vr, refractory=tau_refE)
    decisionI = NeuronGroup(NI, model=eqsI, threshold=Vt, reset=Vr, refractory=tau_refI)
    decisionE.tau = CmE / gLeakE
    decisionI.tau = CmI / gLeakI
    decisionE1 = decisionE.subgroup(N_D1)
    decisionE2 = decisionE.subgroup(N_D2)
    decisionE3 = decisionE.subgroup(N_DN)

    # Connections involving AMPA synapses
    C_DE_DE_AMPA = Connection(decisionE, decisionE, 'gea', delay=d)
    C_DE_DE_AMPA.connect_full(decisionE1, decisionE1, weight=w_p * gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE2, decisionE2, weight=w_p * gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE1, decisionE2, weight=w_m * gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE2, decisionE1, weight=w_m * gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE3, decisionE1, weight=w_m * gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE3, decisionE2, weight=w_m * gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE3, decisionE3, weight=gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE1, decisionE3, weight=gEE_AMPA / gLeakE)
    C_DE_DE_AMPA.connect_full(decisionE2, decisionE3, weight=gEE_AMPA / gLeakE)
    C_DE_DI_AMPA = Connection(decisionE, decisionI, 'gea', weight=gEI_AMPA / gLeakI, delay=d)

    # Connections involving NMDA synapses
    # Note that due to the all-to-all connectivity, the contribution of NMDA can be calculated efficiently
    selfnmda = IdentityConnection(decisionE, decisionE, 'xpre', weight=1.0, delay=d)
    E1_nmda = asarray(decisionE1.spre)
    E2_nmda = asarray(decisionE2.spre)
    E3_nmda = asarray(decisionE3.spre)
    E1_gen = asarray(decisionE1.gen)
    E2_gen = asarray(decisionE2.gen)
    E3_gen = asarray(decisionE3.gen)
    I_gen = asarray(decisionI.gen)

    # Calculate NMDA contributions in each time step
    @network_operation(when='start')
    def update_nmda():
        sE1 = sum(E1_nmda)
        sE2 = sum(E2_nmda)
        sE3 = sum(E3_nmda)
        E1_gen[:] = gEE_NMDA / gLeakE * (w_p*sE1 + w_m*sE2 + w_m*sE3)
        E2_gen[:] = gEE_NMDA / gLeakE * (w_m*sE1 + w_p*sE2 + w_m*sE3)
        E3_gen[:] = gEE_NMDA / gLeakE * (sE1 + sE2 + sE3)
        I_gen[:] = gEI_NMDA / gLeakI * (sE1 + sE2 + sE3)

    # Connections involving GABA synapses
    C_DI_DE = Connection(decisionI, decisionE, 'gi', weight = gIE_GABA / gLeakE, delay = d)
    C_DI_DI = Connection(decisionI, decisionI, 'gi', weight = gII_GABA / gLeakI, delay = d)

    # External inputs
    extinputE1 = PoissonGroup(N_D1, rates=nu_ext_1)
    extinputE2 = PoissonGroup(N_D2, rates=nu_ext_2)
    extinputE3 = PoissonGroup(N_DN, rates=nu_ext)
    extinputI = PoissonGroup(NI, rates=nu_ext)

    # Connect external inputs
    extconnE1 = IdentityConnection(extinputE1, decisionE1, 'gea', weight = gextE / gLeakE)
    extconnE2 = IdentityConnection(extinputE2, decisionE2, 'gea', weight = gextE / gLeakE)
    extconnE3 = IdentityConnection(extinputE3, decisionE3, 'gea', weight = gextE / gLeakE)
    extconnI = IdentityConnection(extinputI, decisionI, 'gea', weight = gextI / gLeakI)

	# Return the integration circuit
    groups = {'DE': decisionE, 'DI': decisionI, 'DX1': extinputE1, 'DX2': extinputE2, 'DX3': extinputE3, 'DXI': extinputI}
    subgroups = {'DE1': decisionE1, 'DE2': decisionE2, 'DE3': decisionE3}
    connections = {'selfnmda': selfnmda,
                   'extconnE1': extconnE1, 'extconnE2': extconnE2, 'extconnE3': extconnE3, 'extconnI': extconnI,
                   'C_DE_DE_AMPA': C_DE_DE_AMPA, 'C_DE_DI_AMPA': C_DE_DI_AMPA, 'C_DI_DE': C_DI_DE, 'C_DI_DI': C_DI_DI }


    return groups, connections, update_nmda, subgroups
wp = 1.65
if __name__ == '__main__':
    import json


    Dgroups, Dconnections, Dnetfunctions, Dsubgroups = make_integration_circuit()


    decisionE = Dgroups['DE']
    decisionI = Dgroups['DI']
    decisionE1 = Dsubgroups['DE1']
    decisionE2 = Dsubgroups['DE2']
    decisionE3 = Dsubgroups['DE3']

    mu0 = 50 * Hz # change
    G_ext_AMPA = 2.1
    G_Leak = 25
    w_ext = G_ext_AMPA / G_Leak * 2
    d = 0.1 * ms
        #d = 0.1 * ms

    stim_on = 300.0 * ms                         # stimulus onset
    stim_off = 800.0 * ms
    runtime = 1500.0 * ms

    import numpy as np

    pred = np.load("pred_amin_normalized.npy") # pred_amin_normalized path
    names = np.load("y_amin_sorted.npy")       # y_amin_sorted path

        # pred = np.vstack((pred[:4], pred[-4:]))
        # pred = pred[]
        # names = names[:10]
        # names = np.hstack((names[:4], names[-4:]))

    y = np.zeros(names.shape[0])
    class_names = ['B', 'F', 'H', 'M', 'Bdn', 'Fdn', 'Hdn', 'Mdn', 'Bda', 'Fda', 'Hda', 'Mda']
    for i in range(names.shape[0]):
        if '\\' in names[i]:
            cls = names[i].split('\\')[-1].split('_')[0]
        else:
            cls = names[i].split('/')[-1].split('_')[0]

        for j in range(len(class_names)):
            if cls == class_names[j]:
                y[i] = j
                break
        else:
            print('class {} not in listed classes'.format(cls))

    animate_selective = [8, 11]
    inanimate_selective = [3, 21]

        # pred[y > 3, :, 3] *= 1.3
        # pred[y > 3, :, 21] *= 1.3
        # pred[y > 3, :, 8] *= 0.7
        # pred[y > 3, :, 11] *= 0.7
        #
        # pred[y <= 3, :, 8] *= 1.3
        # pred[y <= 3, :, 11] *= 1.3
        # pred[y <= 3, :, 3] *= 0.7
        # pred[y <= 3, :, 21] *= 0.7

    animate_all = np.sum(pred[:, :, animate_selective], axis=2)
    inanimate_all = np.sum(pred[:, :, inanimate_selective], axis=2)

        # mean_spike = (animate_all + inanimate_all + 0.01) / 2
    animate_all = (animate_all / animate_all.max()) * mu0
    inanimate_all = (inanimate_all / inanimate_all.max()) * mu0

    animate_all = animate_all[:, 3:]

    inanimate_all = inanimate_all[:, 3:]

    plt.subplot(1, 2, 1)
    plt.title('animate images')
    plt.plot(animate_all[y < 4].T, 'b-')
    plt.plot(inanimate_all[y < 4].T, 'r-')
        # plt.legend()
    plt.subplot(1, 2, 2)
    plt.title('inanimate images')
    plt.plot(animate_all[y > 3].T, 'b-')
    plt.plot(inanimate_all[y > 3].T, 'r-')
        # plt.legend()
    plt.show()

    level_duration = (stim_off - stim_on) / 27
        # print (level_duration)
        # print 'level duration :', level_duration

    def rate1(t):
        global animate
        if t >= stim_on and t < stim_off:
            current_level = int((t - stim_on) / level_duration)
                # print (current_level)
            t = np.random.normal(animate[current_level], 4)
                #print (t)
            return t

        else:
            return 0

    def rate2(t):
        global inanimate
        if t >= stim_on and t < stim_off:
            current_level = int((t - stim_on) / level_duration)
            t = np.random.normal(inanimate[current_level], 4)
            return t
        else:
            return 0


    poisson_input1 = PoissonGroup(len(decisionE1), rates=rate1)
    poisson_input2 = PoissonGroup(len(decisionE2), rates=rate2)

    C_I1_E1_AMPA = IdentityConnection(poisson_input1, decisionE1, 'gea', delay=d, weight=w_ext)
    C_I2_E2_AMPA = IdentityConnection(poisson_input2, decisionE2, 'gea', delay=d, weight=w_ext)

    Dconnections['C_I1_E1_AMPA'] = C_I1_E1_AMPA
    Dconnections['C_I2_E2_AMPA'] = C_I2_E2_AMPA
    Dgroups['poisson_input1'] = poisson_input1
    Dgroups['poisson_input2'] = poisson_input2

    R_DE1 = PopulationRateMonitor(decisionE1, bin=5*ms)
    R_DE2 = PopulationRateMonitor(decisionE2, bin=5*ms)
        # print decisionE1.clock
        # R_DI = PopulationRateMonitor(decisionI, bin=20*ms)

        # S_DE1 = SpikeMonitor(decisionE1, record=True)
        # S_DE2 = SpikeMonitor(decisionE2, record=True)
        # S_DI = SpikeMonitor(decisionI, record=True)

        # ---- set initial conditions (random)

    net = Network(Dgroups.values(), Dconnections.values(),Dnetfunctions, R_DE1, R_DE2)#, R_DI, S_DE1, S_DE2, S_DI)
    net.prepare()

    rates_DE1 = []
    rates_DE2 = []
    rates_DI = []

    spikes_DE1 = []
    spikes_DE2 = []
    spikes_DI = []

    for i in range(600):

        print('---------- image', i, names[i])
        animate = animate_all[i]
        inanimate = inanimate_all[i]

        net.reinit(states=False)

        decisionE.V = -70
        decisionE.gen = 0
        decisionE.gi = 0
        decisionE.spre = 0
        decisionE.xpre = 0
        decisionI.V = -70
        decisionI.gen = 0
        decisionI.gi = 0
        decisionI.gen = 0

            # ---- set initial conditions (random)
        decisionE.gen = decisionE.gen * (1 + 0.2 * rand(decisionE.__len__()))
        decisionI.gen = decisionI.gen * (1 + 0.2 * rand(decisionI.__len__()))
        decisionE.V = decisionE.V + rand(decisionE.__len__()) * 2 * mV
        decisionI.V = decisionI.V + rand(decisionI.__len__()) * 2 * mV

        net.run(runtime, threads=6, report='stdout')

            # plt.figure()
            # plt.subplot(1, 2, 1)
            # plt.title(class_names[int(y[i])] + ' outputs')
            # plt.plot(R_DE1.times / ms, R_DE1.rate, 'b-', label='animate')
            # plt.plot(R_DE2.times / ms, R_DE2.rate, 'r-', label='inanimate')
            # plt.legend()
            # plt.subplot(1, 2, 2)
            # plt.title(class_names[int(y[i])] + ' inputs')
            # plt.plot(animate_all[i], 'b-', label='animate')
            # plt.plot(inanimate_all[i], 'r-', label='inanimate')
            # plt.legend()

        rates_DE1.append(R_DE1.rate)
        rates_DE2.append(R_DE2.rate)
            # rates_DI.append(R_DI.rate)

            # spikes_DE1.append(S_DE1.spiketimes)
            # spikes_DE2.append(S_DE2.spiketimes)
            # spikes_DI.append(S_DI.spiketimes)
            #
            # thresh_pass1 = (R_DE1.rate > 15 * Hz) * 1
            # thresh_pass2 = (R_DE2.rate > 15 * Hz) * 1
            #
            # plt.show()
            # print np.argmax(thresh_pass1), np.argmax(thresh_pass1)
            #
            # if thresh_pass1 > thresh_pass2:
            #     decision = 0
            # else:
            #     decision = 1
            #
            #
            # print('reaction time :', (R_DE1.times[np.argmax(thresh_pass1)] * second) - stim_on)
            # print('reaction time :', (R_DE2.times[np.argmax(thresh_pass2)] * second) - stim_on)
            # print('Decision :', decision)

        # plt.show()

    rates_DE1 = np.array(rates_DE1)
    rates_DE2 = np.array(rates_DE2)
    rates_DI = np.array(rates_DI)
        #
        # # from scipy.io import savemat
        # # savemat('rates.mat', {'DE1': rates_DE1, 'DE2': rates_DE2, 'y': y, 'names': names})
        #
        # spikes_DE1 = np.array(spikes_DE1)
        # spikes_DE2 = np.array(spikes_DE2)
        # spikes_DI = np.array(spikes_DI)
        #
    np.save('R_DE1_amin.npy', rates_DE1)
    np.save('R_DE2_amin.npy', rates_DE2)
    np.save('R_DI_amin.npy', rates_DI)
        # #
        # np.save('S_DE1_amin.npy', spikes_DE1)
        # np.save('S_DE2_amin.npy', spikes_DE2)
    # np.save('S_DI_amin.npy', spikes_DI)
