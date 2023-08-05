from pullrequester.pullrequester import PullRequester
import sys

if __name__ == "__main__":
    pr = PullRequester()
    pr.check_input()
    pr.request_pull(sys.argv[1], sys.argv[2], sys.argv[3])
