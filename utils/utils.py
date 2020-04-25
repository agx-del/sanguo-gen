# coding=utf-8
import sys


def get_all_words_in_article(filename):
    read_cnt = 1
    empty_line_cnt = 0
    lines = []
    words = []
    print("get all words from %s..." % filename, end="")
    sys.stdout.flush()
    with open(filename, 'rb') as f:
        for line in f.readlines():
            if(read_cnt > 100000):
                print("[ERROR]reach max input unit count, exit abnomaly!")
                break
            try:
                content = line.decode('gb18030').strip()
                if (len(content) == 0):
                    empty_line_cnt += 1
                else:
                    lines.append(content)#.strip())
                read_cnt += 1
                if read_cnt % 100 == 0:
                    print(".", end="")
                    sys.stdout.flush()
            except:
                print("[ERROR]read error in line:%d!" % read_cnt)
    print("done!")
    sys.stdout.flush()

    words = "\n".join(lines)
    print("totle none empty line:%d" % (read_cnt-empty_line_cnt))
    return words


def get_all_none_repeated_words(words):
    none_rpt_words = list(set(words))
    print("totle words:%d" % len(words))
    print("none repeated words:%d" % len(none_rpt_words))
    return sorted(none_rpt_words)
