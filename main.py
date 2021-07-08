import matplotlib; matplotlib.use('Agg')
from sdesk.proc import io
import xylib


# Define your method main()
def main():
    # LOAD INPUT FILE
    input_metadata = io.get_input_metadata()
    files = io.get_input_files(input_metadata)
    sdesk_input_file = files[0]
    file_metadata = input_metadata[0]


    # PROCESS THE INPUT FILE AND PRODUCE RESULTS
    file_name = file_metadata['name']
    data = xylib.load_file(sdesk_input_file.path())
    num_blocks = data.get_block_count()
    
    output_blocks = []
    for i in range(num_blocks):
        block = data.get_block(i)
        block_name = block.get_name()
        if not block_name:
            block_name = 'datablock_{}'.format(i)
        numColumns = block.get_column_count()
        maxNumRows = block.get_point_count()
        
        column_names = []
        for c in range(numColumns):
            col = block.get_column(c+1)# i=0 is index column
            if col.get_name():
                col_name = col.get_name()
            else:
                col_name = "Column_" + str(c+1)
            column_names.append(col_name)
            
        rows = []
        for i in range(0,maxNumRows):
            row = []
            for c in range(numColumns):
                col=block.get_column(c+1) # i=0 is index column
                row.append(repr(col.get_value(i)))
            rows.append(row)
        
        output_blocks.append( { 'name': block_name,
                                'rows': rows, 
                                'column_names': column_names})    


    # CREATE THE OUTPUT FILES - THEY WILL DERIVE FROM THE INPUT FILE
    for output_block in output_blocks:
        output_name = "{}.txt".format(output_block['name'])
        sdesk_output_file = io.create_output_file(output_name)
        io.write_tsv_file(sdesk_output_file.path(), output_block['column_names'], output_block['rows'])
           

# Call method main()
main()