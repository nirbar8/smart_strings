# script that mark all files as malicious
for files in os.listdir('floss_output'):
    with open(os.path.join('floss_output', files), 'r') as f:
        data = json.load(f)
    data['is_malicious'] = True
    with open(os.path.join('floss_output', files), 'w') as f:
        json.dump(data, f, indent=4)
