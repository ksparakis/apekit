
# We just need to pass the array of tuples in the correct manner and it should do the rest just fine
# Also pass the total number of apps

# Petar Ojdrovic

import matplotlib.pyplot as plt

def chart_vulns(vulns, total_apps):
    vulnerability, frequency = zip(*vulns)

    explode = (0.01, 0.01)

    colors = ['lightcoral', 'lightskyblue']

    for iterate in xrange(0, len(vulns)):
        ratio = (frequency[iterate] / float(total_apps)) * 100
        remainder = 100 - ratio

        
        label = vulnerability[iterate]
        label1 = "Rest Of Apps"
        
        labels = [label, label1]
        
        templist = [ratio, remainder]
        
        plt.pie(templist, explode=explode, labels=labels, colors=colors)
     
        plt.axis('equal')
        plt.show()
    
