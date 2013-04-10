from __future__ import print_function
import sys, os, time


def get_files(directory, board_family):
    return [os.path.normpath('./%s/%s' % (board_family, f)) for f in os.listdir(directory) if f[-2:] == '.b']

def create_report(times, test_file, board_family):

    average = sum([time for test, time in times.iteritems() if test != 'total']) / len(times)
    max_time = max([time for test, time in times.iteritems() if test != 'total'])

    r = ""
    r += "Running times for %s on %s\n\n" % (test_file, board_family)
    r += "Total = %.3f\n" % times['total']
    r += "Average time = %.3f\n" % average
    r += "Longest time = %.3f" % max_time
    r += "\n\n--------------------------------------------------\n\n"


    for k,v in times.iteritems():
        if k != 'total':
            r += "%s\t:\t%.3fs\n" % (k,v)

    print(r)

    with open(os.path.normpath('../timing_reports/%s_%s.txt' % (board_family, test_file[:-3]) ), 'w') as f:
        f.write(r)

    return r


def main():
    if len(sys.argv) < 3:
        print("Peter Zenger's Timing Program")
        print("Usage: %s [PATH TO .PY FILE] [PATH TO BOARD DIRECTORY]" % sys.argv[0])
        sys.exit(-1)

    test_file = sys.argv[1]
    board_family = sys.argv[2]
    directory = os.path.normpath('%s' % sys.argv[2])
    boards = get_files(directory, board_family)

    times = {}

    start_time = time.clock()
    for board in boards:
        board_start = time.clock()
        os.system('python %s %s' % (test_file, board))
        board_total = time.clock() - board_start
        times[board] = board_total

    total_time = time.clock() - start_time
    times['total'] = total_time

    create_report(times, test_file, board_family)
    print("DING DONE")


if __name__ == "__main__":
    main()