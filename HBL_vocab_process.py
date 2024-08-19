"""Script for pulling out vocab from hambaanlaang"""



import numpy as np
import pandas as pd
import glob
import os


# list of weird characters that end up as keys
weird = ["：", "「", "」", "﹗", "？", "，", "。", "……", "{}", "、", "！", "︰"]

story_id = pd.read_csv("HBL_story_list.csv", names=["ID", "level"], dtype={'ID': str, 'level': int})


# TODO: need a csv (or multiple) that gives me the names of the stories to match to levels
#level1 = ["00002", "00261", "00014", "00034", "00026", "00013", "00258", "00260", "00266", "00259", "00257", "00256", "00265", "00262", "00267", "00263", "00268", "00270", "00277", "00264"] 

LEVEL = 7  # max level
folder = "../stories/legacy/sheets"  # NOTE: path for the HBL stories
total = {}
for ldx in range(1, LEVEL + 1):
    level = story_id[story_id.level == ldx].ID.values.tolist()


    filenames = []
    for ll in level:
#        print(ll)
        ggg = glob.glob(os.path.join(folder, "*" + ll + "*"))
        try:
            filenames.append(ggg[0])
        except IndexError as e:
            pass

    for flnm in filenames:
#        print(flnm)

        df = pd.read_csv(flnm, names=np.arange(50))
#        print(df)


        # make a list of dictionaries
        b = [] # empty list
        for bb in range(int(df.shape[0]/3)):
            try:
                a = {df.loc[1 + 4*bb + 0].values[i]:\
                      [df.loc[1 + 4*bb + 1].values[i], df.loc[1 + 4*bb + 2].values[i], ldx]\
                        for i in range(20)}
                b.append(a)
            except KeyError as e:
                pass

        #print(b)

        # merge the list of dictionaries
        # NOTE: checking if key already in total will get slow... but, who cares...
        f = {}
        for bb in b:
#            print(bb)
            for key in bb:
                if key not in total:
                    tmp = bb[key]
                    tmp.append(1)
                    f.update({key: tmp})
                else:
                    print(key)
                    tmp = total[key]
                    print(tmp)
                    tmp[-1] = tmp[-1] + 1
                    total[key] = tmp 
#                    print(key, "already in total")


        # special treatment to remove the NaNs
        g = f.copy()
        for key in f:
            #print(key, f[key])

            # remove NaNs
            try:
                if np.isnan(key):
                    del g[key]
            except:
                pass

            # remove weird characters
            try:
                if key in weird:
                    del g[key]
            except:
                pass

            # remove names 
            try:
                if "Aa3-" in g[key][0]:
                    del g[key]
            except:
                pass


            try:
                if "#" in g[key][0]:
                    del g[key]
            except:
                pass



        print(g)
         

    #    for key in g:
    #        g0, g1 = g[key]
    #        print(key, g0, g1)


        total.update(g)


#    print("final dict")
#    print(total)


#    for key in total:
#        g0, g1, g3, g4 = total[key]
#        print(key, g0, g1, g3)


# FIXME: problem with level, is that the dictionary stores only the latest occurance
#        so putting all text together, just tells me the last story it appeared in...
# can I get update to keep the first?


# NOTE: strip out text after hash
for key in total:
    tmp = total[key]
    print(tmp)
    if '#' in tmp[1]:
        print("here!")
        tmp[1] = tmp[1].split('#')[0]
    total[key] = tmp


print("test!")
tmp = pd.DataFrame.from_dict(total, orient="index")#, columns=["Chinese", "jyutping", "English"])
tmp = tmp.reset_index()
tmp.columns = ["Chinese", "jyut6ping3", "English", "HBLlevel", "frequency"]
#tmp.to_csv(os.path.join("vocab", "HBL_vocab.csv"),
#           index=False, header=False)
tmp.to_csv("HBL_vocab.csv", index=False, header=False)

# separate per level
for ldx in range(1, LEVEL + 1):

    #tmp[tmp.HBLlevel == ldx].to_csv(os.path.join("vocab", "HBL_vocab_" + str(ldx) + ".csv"),
    #                                index=False, header=False)
    tmp[tmp.HBLlevel == ldx].to_csv("HBL_vocab_" + str(ldx) + ".csv", index=False, header=False)


