from pathlib import Path
import time
import csv

def write_profile_info_in_file(profile, file_name):
    with open(file_name, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        ## write profile
        wr.writerow(profile)
    fp.close()

def read_csv (file_name):
    l = []
    script_dir = Path(__file__).parent
    with open(str(script_dir)+'/'+ str(file_name)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            l.append(row)
    return l

def main():

        profiles = read_csv('profiles.csv')
        for profile in profiles:
            new_profile = []
            xps = profile[5].split(',')
            educations = profile[6].split(',')
            new_profile.append(profile[0])
            new_profile.append(profile[1])
            new_profile.append(profile[2])
            new_profile.append(profile[3])
            new_profile.append(profile[4])
            for xp in xps:
                new_profile.append(xp)
            new_profile.append('   ')
            for edu in educations:
                new_profile.append(edu)
            new_profile.append('   ')
            new_profile.append(profile[7])
            write_profile_info_in_file(new_profile, 'final_result.csv')

main()