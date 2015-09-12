__author__ = 'Andrew'

# No need to process files and manipulate strings - we will
# pass in lists (of equal length) that correspond to
# sites views. The first list is the site visited, the second is
# the user who visited the site.

# See the test cases for more details.


def highest_affinity(site_list, user_list, time_list):
  # Returned string pair should be ordered by dictionary order
  # I.e., if the highest affinity pair is "foo" and "bar"
  # return ("bar", "foo").

    D = {}
    sites = set()

    for i in range(0,len(site_list)):
        site = site_list[i]
        user = user_list[i]
        sites.add(site)
        if site in D:
            D[site].add(user)
        else:
            D[site] = set()
            D[site].add(user)

    #print D
    affinities = {}
    max = -1;

    for site1 in sites:
        for site2 in sites:
            if site1 != site2:
                affinity = len(D[site1] & D[site2])
                #affinities[(site1,site2)] = affinity
                if affinity > max:
                    max = affinity
                    answer = [site1,site2]
                    answer.sort()

    answer = tuple(answer)
    #print answer

    #print affinities
    return answer








    #return ('abc', 'def')
