max_id = 'T0003'
new_id = max_id[:1] + str(int(max_id[1:]) + 1).zfill(len(max_id) - 1)
print(new_id)