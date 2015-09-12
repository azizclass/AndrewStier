__author__ = 'Andrew'

# No need to process files and manipulate strings - we will
# pass in lists (of equal length) that correspond to
# sites views. The first list is the site visited, the second is
# the user who visited the site.

# See the test cases for more details.

alist = [1,2,3]
print alist[0]

for x in range(0, 3):
    print "We're on time %d" % (x)

def highest_affinity(site_list, user_list, time_list):
  # Returned string pair should be ordered by dictionary order
  # I.e., if the highest affinity pair is "foo" and "bar"
  # return ("bar", "foo").

    for i in range(0,len(site_list)-1):
        print site_list[i]
        print user_list[i]



    return ('abc', 'def')
