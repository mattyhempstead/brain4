import time


class Haptic_Errors(Exception):
    pass

class No_Mapping_Error(Haptic_Errors):
    def __init__(self, missing_char):
        self.missing_char = missing_char
        self.message = "Selected character \'{}\' does not have a mapping, update char_grid_mapper.txt".format(missing_char)
        super().__init__(self.message)

class Haptic_Relayer:
    def __init__(self, mapping_fileName="char_grid_mapper.txt"):
        self.mapping_fileName = mapping_fileName
        self.input_set_grid_map = self.build_grid_map()
        self.current_grid = self.input_set_grid_map["''"]

    def relay_text_from_keyboard(self, selected_char):
        try:
            if selected_char not in self.input_set_grid_map:
                raise No_Mapping_Error(selected_char)
            
            else:
                self.current_grid = self.input_set_grid_map["{}".format(selected_char)]
                self.relay_text_to_user()
                
        
        except No_Mapping_Error:
            print(No_Mapping_Error)

    def relay_text_to_user(self):
        """
        Future Work When Haptic Hardware is ready:
        1) Replace first grid_test_printer statement with function which moves the metal rods according to self.current_grid 
        2) Replace second grid_test_printer statement with function which moves the metal rods according to self.current_grid (this has been reset to default)
        """

        #Replace next two lines when hardware is ready
        print("-------------Selected Character is----------------")
        self.grid_test_printer(self.current_grid)
        
        time.sleep(1.5)
        self.current_grid = self.input_set_grid_map["''"]

        #Replace next two lines when hardware is ready
        print("-------------Reseting grid to----------------")
        self.grid_test_printer(self.current_grid)
    
    def build_grid_map(self):
        grid_map = {}
        mapping_file = open(self.mapping_fileName, "r")
        for line in mapping_file.readlines():
            char , mapping  = line.rstrip("\n").split("::")
            grid_map[char]=mapping
        
        return grid_map

    def grid_test_printer(self, mapping):
        line_ctr = 0
        for char in mapping[1:len(mapping)-1]:
            if char == '0':
                char = ' '
            print(char, end='')
            line_ctr+=1
            if line_ctr%16 == 0:
                print()
        
        print()

hpt = Haptic_Relayer()
hpt.relay_text_from_keyboard("1")
hpt.relay_text_from_keyboard("A")