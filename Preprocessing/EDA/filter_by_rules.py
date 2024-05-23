from Preprocessing.ultils.common_ import type_map
import os, csv, ast, shutil
from Preprocessing.ultils.spellcheck import validate_TOTAL_COST_amount

inv_type_map = {v: k for k, v in type_map.items()}

keywords_TIMESTAMP = ['ngày', 'thời gian', 'giờ']
keywords_TOTAL_COST = ['tổng tiền', 'cộng tiền hàng', 'tổng cộng', 'thanh toán', 'tại quầy']

def filter_by_rules(csv_file, output_csv_file, output_filtered_dir, img_dir=None):
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        first_line = True
        total_wrong_key = 0
        total_many_few_key = 0
        output_rows = []

        for n, row in enumerate(csv_reader):
            if first_line:
                first_line = False
                output_rows.append(row)
                continue
            if n < 0:
                continue
            
            img_name = row[0]
            boxes = ast.literal_eval(row[1])
            key, value = row[3].split('|||'), row[2].split('|||')
            num_box, score = row[4], row[5]
            ignore_file = False

            # Modify wrong key by rules
            filter_wrong_key = True 
            if filter_wrong_key:
                for idx, val in enumerate(value):
                    val_lower = val.lower()
                    for kw in keywords_TIMESTAMP:
                        if kw in val_lower and key[idx] != 'TIMESTAMP':
                            total_wrong_key += 1
                            print(total_wrong_key, img_name, 'filter_training_data_by_rules_Fixed', key[idx], '=>', 'TIMESTAMP')
                            key[idx] = 'TIMESTAMP'
                            boxes[idx]['category_id'] = inv_type_map['TIMESTAMP']

                    for kw in keywords_TOTAL_COST:
                        if kw in val_lower and key[idx] != 'TOTAL_COST':
                            total_wrong_key += 1
                            print(total_wrong_key, img_name, 'filter_training_data_by_rules_Fixed', key[idx], '=>', 'TOTAL_COST')
                            key[idx] = 'TOTAL_COST'
                            boxes[idx]['category_id'] = inv_type_map['TOTAL_COST']

                for jdx, val in enumerate(value):
                    val_lower = val.lower()
                    if validate_TOTAL_COST_amount(val_lower) and key[jdx] == 'TIMESTAMP':
                        total_wrong_key += 1
                        print(total_wrong_key, img_name, val_lower, 'filter training data by rules fixed', key[jdx], '=>', 'TOTAL_COST')
                        key[jdx] = 'TOTAL_COST'
                        boxes[jdx]['category_id'] = inv_type_map['TOTAL_COST']

            num_keys = {'SELLER': 0, 'ADDRESS': 0, 'TIMESTAMP': 0, 'TOTAL_COST': 0}
            for idx, k in enumerate(key):
                if k in num_keys.keys():
                    num_keys[k] += 1
                else:
                    print(img_name, 'filter training data by rules Wrong key', k)

            # Filter too many keys for TOTAL_COST
            filter_too_many_keys = True
            if filter_too_many_keys:
                if num_keys['TOTAL_COST'] > 4:
                    total_many_few_key += 1
                    print(total_many_few_key, img_name, 'filter training data by rules Too many TOTAL_COST')
                    ignore_file = True

            # Filter too few keys
            filter_too_few_keys = True
            if filter_too_few_keys:
                total_exist_key = sum(1 for k in num_keys if num_keys[k] > 0)
                if total_exist_key < 3:
                    total_many_few_key += 1
                    ignore_file = True
                    print(total_many_few_key, img_name, 'filter training data by rules Very few TOTAL_COST')

            if not ignore_file:
                row[1] = str(boxes)
                row[3] = '|||'.join(key)
                row[2] = '|||'.join(value)
                output_rows.append(row)
                shutil.copy(os.path.join(img_dir, img_name), os.path.join(output_filtered_dir, img_name))
            else:
                print(n, 'ignore', img_name)

        with open(output_csv_file, mode='w', newline='') as outfile:
            csv_writer = csv.writer(outfile, delimiter=',')
            csv_writer.writerows(output_rows)
        print('DONE!!!!')


