#!/usr/bin/env python3

# from multiprocessing.pool import Pool
import logging
import argparse
#import matplotlib
#matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ca
#######################################################
logfile = 'log.txt'
logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Mohcine Chraibi'), bitrate=1800)


def get_parser_args():
    parser = argparse.ArgumentParser(
        description='Cellular Automaton. Floor Field Model [Burstedde2001] Simulation of pedestrian'
                    'dynamics using a two-dimensional cellular automaton Physica A, 295, 507-525, 2001')
    parser.add_argument('-s', '--ks', type=float, default=2,
                        help='sensitivity parameter for the  Static Floor Field (default 2)')
    parser.add_argument('-d', '--kd', type=float, default=1,
                        help='sensitivity parameter for the  Dynamic Floor Field (default 1)')
    parser.add_argument('-n', '--numPeds', type=int, default=10, help='Number of agents (default 10)')
    parser.add_argument('-p', '--plotS', action='store_const', const=True, default=False,
                        help='plot Static Floor Field')
    parser.add_argument('--plotD', action='store_const', const=True, default=False,
                        help='plot Dynamic Floor Field')
    parser.add_argument('--plotAvgD', action='store_const', const = True, default=False,
                        help='plot average Dynamic Floor Field')
    parser.add_argument('-P', '--plotP', action='store_const', const=True, default=False,
                        help='plot Pedestrians')
    parser.add_argument('-r', '--shuffle', action='store_const', const=True, default=True,
                        help='random shuffle')
    parser.add_argument('-v', '--reverse', action='store_const', const=True, default=False,
                        help='reverse sequential update')
    parser.add_argument('-l', '--log', type=argparse.FileType('w'), default='log.txt',
                        help='log file (default log.txt)')
    parser.add_argument('--decay', type=float, default=0.3,
                        help='the decay probability of the Dynamic Floor Field (default 0.2')
    parser.add_argument('--diffusion', type=float, default=0.1,
                        help='the diffusion probability of the Dynamic Floor Field (default 0.2)')
    parser.add_argument('--maxframe', type=int, default=1000,
                        help='Max simulation frame  (default 1000)')

    parser.add_argument('-W', '--width', type=float, default=4.0,
                        help='the width of the simulation area in meter, excluding walls')
    parser.add_argument('-H', '--height', type=float, default=4.0,
                        help='the height of the simulation room in meter, excluding walls')

    parser.add_argument('-c', '--clean', action='store_const', const=True, default=False,
                        help='remove files from directories dff/ sff/ and peds/')

    parser.add_argument('-N', '--nruns', type=int, default=1,
                        help='repeat the simulation N times')

    parser.add_argument('--parallel', action='store_const', const=True, default=False,
                        help='use multithreading')
    parser.add_argument('--save', action='store_const', const=True, default=False,
                        help='save movie')

    parser.add_argument('--moore', action='store_const', const=True, default=False,
                        help='use moore neighborhood. Default= Von Neumann')

    parser.add_argument('--box', type=int, nargs=4, default=None,
                        help='Rectangular box, initially populated with agents: from_x, to_x, from_y, to_y. Default: The whole room')

    _args = parser.parse_args()
    return _args

pause = False

def pause_anim(event):
    global pause, ani
    pause ^= True
    if pause:
        ani.event_source.stop()
        print("Animation paused")
    else:
        ani.event_source.start()

def stop_anim(event):
    global ani, fig
    print("end of simulation")
    ani.event_source.close()
    ani.event_source.stop()

if __name__ == "__main__":
    parser_args = get_parser_args()
    CA = ca.automaton(parser_args)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    CA.image = CA.plot_peds(fig, ax)
    ani = animation.FuncAnimation(fig, CA.update, interval=10, blit=True, frames=CA.max_frame+1, repeat=True)

    fig.canvas.mpl_connect('close_event', stop_anim)
    fig.canvas.mpl_connect('button_press_event', pause_anim)
    fig.canvas.mpl_connect('key_press_event', pause_anim)


    if not parser_args.save:
        plt.show()
    if  parser_args.save:
        ani.save('ca.mp4', writer=writer)
        print(">> saved: ca.mp4")

    CA.print_logs()
