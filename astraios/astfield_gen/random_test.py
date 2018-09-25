import random

def ran_exp_list(mean, num):
	count = 0
	total = 0
	num_list=[]
	while count < num:
		x = random.expovariate(1/mean)
		if x < 7:
			continue
		num_list.append(x)
		total += x
		count += 1
	print("----")
	print("Average",total/num)
	num_list = sorted(num_list)
	print("Max",num_list[-5:-1])
	print("Min",num_list[0])
	return num_list

mean_num = int(input("Mean? "))
number = int(input("Number? "))

ran_exp_list(mean_num,number)
