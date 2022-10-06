"""
python predictions-cli.py -c a7f84cb "Does he win?" 120 yes no
python predictions-cli.py --create 236472364 Win? "he wins!" 30 "No shot." "what?"
python predictions-cli.py -n a7f84cb
python predictions-cli.py --cancel 236472364
python predictions-cli.py -r a7f84cb 1
python predictions-cli.py --resolve 236472364 0
python predictions-cli.py -l a7f84cb
python predictions-cli.py --lock 236472364


or import predictions-cli for python programs

from predictions-cli import Prediction
p = Prediction(["Hell yea", 'nah', "draw"], 120)
time.sleep(10)
p.lock()

r = random.random()
if r < 0.1:
	p.cancel()
elif r < 0.6:
	p.resolve(0)
else:
	p.resolve(1)

p.resolve(2) # raises PredictionTerminatedError
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description='CLI interface for Twitch predictions')
    parser.add_argument('-c', '--create', type=str, nargs='+', help='Create a prediction: -c <unique_id> <title(:25)> <prediction window seconds:1-1800> <outcome_1(:25)> <outcome_2(:25)> ... <outcome_10(:25)>')
    parser.add_argument('-l', '--lock', type=str, nargs=1, help='Lock a prediction: -l <id>')
    parser.add_argument('-n', '--cancel', type=str, nargs=1, help='Cancel a prediction: -n <id>')
    parser.add_argument('-r', '--resolve', type=str, nargs=2, help='Resolve a prediction: -r <id> <outcome_index>')
    args = parser.parse_args()

    if args.create:
        if len(args.create) < 5:
            parser.error('Create requires at least 5 arguments')

        if len(args.create) > 13:
            parser.error('Create takes at most 13 arguments')

        try: 
            args.create[2] = int(args.create[2])

        except ValueError:
            parser.error('Prediction window must be an integer in the interval [1, 1800]')

        if args.create[2] < 1 or args.create[2] > 1800:
            parser.error('Prediction window must be an integer in the interval [1, 1800]')

        #create_prediction(args.create)
        print(f'Create prediction: {args.create}')


    elif args.cancel:
        #cancel_prediction(args.cancel)
        print(f'Cancel prediction: {args.cancel}')

    elif args.resolve:
        try:
            args.resolve[1] = int(args.resolve[1])

        except ValueError:
            parser.error('Outcome index must be an integer in the interval [0, 9]')

        if args.resolve[1] < 0 or args.resolve[1] > 9:
            parser.error('Outcome index must be an integer in the interval [0, 9]')

        #resolve_prediction(args.resolve)
        print(f'Resolve prediction: {args.resolve}')

    elif args.lock:
        #lock_prediction(args.lock)
        print(f'Lock prediction: {args.lock}')

    else:
        parser.print_help()


if __name__ == '__main__':
    main()