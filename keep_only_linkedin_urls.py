import csv
from pathlib import Path


def read_csv (file_name):
    l = []
    script_dir = Path(__file__).parent
    with open(str(script_dir)+'/'+ str(file_name)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            l.append(row)
    return l   

def write_profiles_info_in_file(profiles, file_name):
    with open(file_name, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        for elem in profiles:
            ## write profile
            wr.writerow(elem)
    fp.close()   

def keep_only_linkedin_urls():
    all_urls = read_csv('linkedin_urls.csv')

    # only keep the linkedin urls
    i = 0
    while i< len(all_urls):
        j = 0
        while j < len(all_urls[i]):
            if all_urls[i][j][0:24] == 'https://translate.google' or all_urls[i][j]=='https://www.linkedin.com/feed/?trk=people-guest_profile-result-card_result-card_full-click':
                all_urls[i].pop(j)
            else:
                j += 1
        i +=1
    
    write_profiles_info_in_file(all_urls, 'only_linkedin_urls.csv')
