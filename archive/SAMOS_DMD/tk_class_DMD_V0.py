#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 10:49:37 2021

@author: robberto
"""
import tkinter as tk
## -- IMPORTS
import os
import socket

import matplotlib.pyplot as plt
import numpy as np



class DMD(tk.Toplevel):     #the DMD class inherits from the tk.Toplevel widget
#    def __init__(self, master=None):
    def __init__(self, master=None):  #__init__ constructor method. 
        #>>> AM = DMD(master) would be an instance of the class DMD that you can call with its functions, e.g.
        #>>> AM.show_Simbad()
    
       # logger = log.get_logger("example1", log_stderr=True)
        #self.logger = logger
        
        super().__init__(master = master) 
        #super() recalls and includes the __init__() of the master class (tk.Topelevel), so one can use that stuff there without copying the code.
        
        
        self.title("DMD")
        self.geometry("1380x1320")
#        label = tk.Label(self, text ="This is the DMD Window")
#        label.pack()

  
#       
        self.frame0l = tk.Frame(self)#, width=300, height=300)
        self.frame0l.place(x=0, y=0, anchor="nw", width=1380, height=1320)
        
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
 #       self.master.title("IDG - PCM module driver")

        # allowing the widget to take the full space of the root window
        #self.pack(fill=tk.BOTH, expand=1)

        self.Echo_String = tk.StringVar()         
        #self.check_if_power_is_on()  
        self.is_on = False
  
# =============================================================================
#         
#         #initialize and (possibly) get echo from DMD
# =============================================================================
        Button_Initialize_DMD = tk.Button(self.frame0l, text="Initialize_DMD",command=self.initialize, relief=tk.RAISED)
        Button_Initialize_DMD.place(x=10,y=10)
        self.Echo_String = tk.StringVar()        
        Label_Echo_Text = tk.Label(self.frame0l,textvariable=self.Echo_String,width=15,bg='white')
        Label_Echo_Text.place(x=160,y=13)
        
# =============================================================================
#         
#         #_open/close  DMD
# =============================================================================
        Button_open_DMD = tk.Button(self.frame0l, text="open_DMD",command=self._open, relief=tk.RAISED)
        Button_open_DMD.place(x=10,y=40)
        Button_close_DMD = tk.Button(self.frame0l, text="close_DMD",command=self._close, relief=tk.RAISED)
        Button_close_DMD.place(x=160,y=40)


# =============================================================================
#         
#         #apply_blackout  DMD
# =============================================================================
        Button_apply_blackout_DMD = tk.Button(self.frame0l, text="apply blackout",command=self.apply_blackout, relief=tk.RAISED)
        Button_apply_blackout_DMD.place(x=10,y=70)
 
# =============================================================================
#         
#         #apply_whiteoutout  DMD
# =============================================================================
        Button_apply_whiteout_DMD = tk.Button(self.frame0l, text="apply whiteout",command=self.apply_whiteout, relief=tk.RAISED)
        Button_apply_whiteout_DMD.place(x=160,y=70)

# =============================================================================
#         
#         #show_current_DMD_shape
# =============================================================================
        Button_show_current_DMD_shape = tk.Button(self.frame0l, text="show current DMD shape",command=self.show_current_DMD_shape, relief=tk.RAISED)
        Button_show_current_DMD_shape.place(x=10,y=100)
        self.current_DMD_shape_String = tk.StringVar()        
        Label_current_DMD_shape = tk.Label(self.frame0l,textvariable=self.current_DMD_shape_String,width=15,bg='white')
        Label_current_DMD_shape.place(x=220,y=102)

# =============================================================================
#         
#         #send command to the DMD
# =============================================================================
        Button_send_command_DMD = tk.Button(self.frame0l, text="send command to DMD",command=self.send, relief=tk.RAISED)
        Button_send_command_DMD.place(x=10,y=130)
        self.command_DMD_String = tk.StringVar()        
        Text_command_DMD = tk.Entry(self.frame0l,textvariable=self.command_DMD_String,width=15,bg='white')
        Text_command_DMD.place(x=200,y=130)


# =============================================================================
#      HANDLE DMD MAP
# 
# =============================================================================
        Button_load_RADEC_list = tk.Button(self.frame0l, text="load RADEC list",command=self.load_RADEC_list, relief=tk.RAISED)
        Button_load_RADEC_list.place(x=800,y=10)

        Button_convert_RADEC_to_CCD_pixels = tk.Button(self.frame0l, text="convert RADEC to pixels",command=self.convert_RADEC_to_pixels, relief=tk.RAISED)
        Button_convert_RADEC_to_CCD_pixels.place(x=800,y=40)

        Button_convert_CCD_pixels_to_DMD = tk.Button(self.frame0l, text="convert pixels to DMDs",command=self.convert_pixels_to_DMDs, relief=tk.RAISED)
        Button_convert_CCD_pixels_to_DMD.place(x=800,y=70)
        
        Button_create_DMD_shape = tk.Button(self.frame0l, text="create DMD shape",command=self.create_DMD_shape, relief=tk.RAISED)
        Button_create_DMD_shape.place(x=800,y=100)

        Button_load_DMD_shape = tk.Button(self.frame0l, text="load DMD shape",command=self.load_DMD_shape, relief=tk.RAISED)
        Button_load_DMD_shape.place(x=800,y=130)
        
# =============================================================================
#      SHIW THE DMD MAP
# 
# =============================================================================
        Canvas_DMD = tk.Canvas(self.frame0l, width=1080, height=1080, bg='dark gray')
        Canvas_DMD.place(x=290,y=5)

    instrument_lib = socket
     
    def initialize(self, config_id='dlp_7000', address='prolix.dynamic-dns.net', port=1000,
                   start_on_whiteout=True, max_diff=786432, dmd_size=(768, 1024), 
                   display_type=32, dmd_data_path='.'):
        """ Initial function for the DMD Controller."""

        self.address = address
        self.port = port
        
        self.start_on_whiteout = start_on_whiteout
        self.dmd_size = dmd_size
        self.max_diff = dmd_size[0]*dmd_size[1] if max_diff is None else max_diff
        self.display_type = display_type
        self.dmd_data_path = dmd_data_path
        
        self._shapes = {'blackout': (np.zeros(self.dmd_size), self.apply_blackout), 
                        'whiteout': (np.ones(self.dmd_size), self.apply_whiteout)}
                        # add more if any other common shapes pop up? 
        self.current_dmd_shape = None

    def _open(self):
        """ Opens a connection to the DMD device. The socket connection will
        time out after a few seconds of inactivity, so this is less opening a
        constant connection and more testing our connection method responds as
        expected."""

        # Connection is reset every ~10 seconds
        instrument = self.instrument_lib.socket(self.instrument_lib.AF_INET, self.instrument_lib.SOCK_STREAM)
        instrument.connect((self.address, self.port))

        # If we get this far, a connection has been successfully opened.
        # Set self.instrument so that we can close if anything here subsequently fails.
        self.instrument = instrument

        # Send a test message to make sure this worked 
        instrument.sendall(':TEST\n')
        response = instrument.recv(20)
        if 'INVALID' not in response:
            raise ConnectionError(f'The socket is not responding as expected, test message responded with {response}.')
        
        # Apply a whiteout to start 
        if self._start_on_whiteout:
            self.apply_whiteout()
     
    def _close(self):
        self.instrument.close()

    def show_current_DMD_shape(self):
        self.show_current_DMD_shape_String.set('current DMD shape...')
        self.instrument.close()

    @property
    def shapes(self):
        """ Make a property so our core shapes are indeditable."""
        return self._shapes

    def send(self):
        command = self.command_DMD_String.get()
        """ Send a message to the controller and check the controller
        sucessfully received it."""

        # reinstantiate connection since it times out
        instrument = self.instrument_lib.socket(self.instrument_lib.AF_INET, self.instrument_lib.SOCK_STREAM)
        instrument.connect((self.address, self.port))
        
        # Check the command message type
        message_type = command[4]

        # Send command
        instrument.sendall(command.encode())
        response = str(instrument.recv(30))
        
        # Make sure we successfully send the command, and the message type matches
        if 'SUCCESS' in response and message_type in response:
            # log or print?
            print(f'Message: {command[:-1]} sucessfully written.')
        elif 'INVALID COMMAND' in response:
            raise ValueError("An invalid command was sent to the controller.")
        elif response == b'':
            raise RuntimeError("The controller is not responding as if a message was sent.")
        else:
            raise RuntimeError(f"Message {command} failed in an unexpected way with {response}.")
    
    def apply_shape_to_both(self, dm1_shape, dm2_shape):
        """ Builtin function for the DeformableMirror class. """
        pass
    
    def apply_whiteout(self):
        """ Apply a full whiteout to the DMD. (All zeros, no mirrors flipped.) """
        
        message = [':00200000000020C0\n',
                   ':0801000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF77\n',
                   ':00230001000300D9\n',
                   ':0007000000F9\n']
        
        for m in message:
            self.send(m)
        
        self.current_dmd_shape = np.copy(self.shapes['whiteout'][0])
        self.update_dmd_plot()

    def apply_blackout(self):
        """ Apply a full blackout to the DMD. (All ones, all mirrors flipped.) """
        message = [':00200000000020C0\n',
                   ':08010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000F7\n',
                   ':00230001000300D9\n',
                   ':0007000000F9\n']
        for m in message:
            self.send(m)

        self.current_dmd_shape = np.copy(self.shapes['blackout'][0])
        self.update_dmd_plot()

    def apply_current(self):
        """ Noop function to map the "current" shape of the DMD to a function. """
        pass

    def apply_shape(self, dm_shape, dm_num=1):
        """ Function to apply a shape to the DMD. The DMD controller can set a
        row and repeat said row. The logic here to optimize does the following :
        
        1. Checks the specified shape against a few preloaded patterns. (Right
        now there's just all white/all black, but those patterns can be updated
        as needed.
        2. Figures out what rows need to be changed given we preset the closet
        pattern. 
        3. Figures out if any of those rows are the same and can be set with a
        repeat row command. 

        For example, if you wanted to set one column to black, we'd start with
        a whiteout, apply the first one with one black pixel, and repeat that
        row all the way down the controller. This would take 4 messages.
        (Start, apply row, repeat row, update and refresh controller.)

        We can set every row individually. Having tested a handful of examples,
        this takes 2ish minutes.

        Parameters
        ----------
        dm_shape : np.array
            Array of 1s/0s to apply to the DMD.
        dm_num : int
            Required parameter from DeformableMirror class.
        """
        
        self.update_dmd_plot(shape=dm_shape, plot_name='attempted_dmd_shape')

        if dm_shape.shape != self.dmd_size:
            raise IndexError(f"Given shape to apply to DMD is of size {dm_shape.shape}, while we expect the DMD to be of size {self.dmd_size}.")

        def find_closest_match(dm_shape):
            """ Find the closest default pattern."""

            if self.current_dmd_shape is not None:
                self._shapes['current'] = (self.current_dmd_shape,
                        self.apply_current)
            
            min_shape_diff = self.max_diff
            shape_key = None
            
            # Loop through and iteratively reset until we have the lowest deviation
            for shape_key in self.shapes.keys():
                shape = self.shapes[shape_key][0]
                shape_diff = np.absolute(shape - dm_shape)
                
                if np.sum(shape_diff) < min_shape_diff:
                    row_adjustment = np.where(np.sum(shape_diff, axis=1) > 0)
                    min_shape_diff = np.sum(shape_diff)
                    shape_function = self.shapes[shape_key][1]

            return shape_function, row_adjustment
          
        # Apply starting shape
        pre_shape, rows = find_closest_match(dm_shape)
        pre_shape()
        rows = rows[0]

        # If we have notable deviation from that starting shape 
        if len(rows) > 0:

            messages = []
            # Start message to set default + display type
            messages.append(self._build_message(data=self.display_type))
            
            n = 0
            # Iterate through the pattern rows
            while n < len(dm_shape):
                
                # Build a message (only) for each row that diverges
                if n in rows:
                    
                    # Check for repeated rows to save on commands
                    sums = np.sum(dm_shape != dm_shape[n], axis=1)
                    row_sums = np.array([np.sum(sums[n:n+i]) for i in range(1, len(sums)-n)])
                    
                    # Pad the end so we can pick up repeats at the bottom of the DMD
                    row_sums = np.array([elem for elem in row_sums] + [1])
                    indices = np.where(row_sums > 0)[0]
                    index = np.min(indices) if len(indices) > 0 else len(indices) + 1
                    
                    # Specify a single row with command
                    row_content = dm_shape[n]
                    messages.append(self._build_message(data_length=int(len(row_content)/8),
                                                        command_type=1, row=n, 
                                                        data=row_content))

                    if index > 1:
                        # Apply that row index - 1 times with command
                        messages.append(self._build_message(data_length=2,
                            command_type=3, row=n+1, data=int(index-1)))
                        
                        # And move forward in the rows to where we are now
                        n += index
                    
                    # Otherwise we only scootch one position forward
                    else:
                        n += 1
                
                # And likewise
                else:
                    n += 1

            # End / refresh message
            messages.append(self._build_message(data_length=0, command_type=7))
            for message in messages:
                self.send(message)
            
            # Update internal track of the DMD shape
            for row in rows:
                row_content = dm_shape[row]
                self.current_dmd_shape[row] = row_content
            
            self.update_dmd_plot()
        
        else:
            print(f'Shape perfectly matches {pre_shape.__name__} preset.')
    
    def update_dmd_plot(self, shape=None, plot_name='current_dm_state'):
        """ Consistent plotting method to write out DMD plot. """
        
        # No shape input means we plot out the current DMD shape.
        shape = shape if shape is not None else self.current_dmd_shape
        
        plt.clf()
        plt.imshow(shape, vmin=0, vmax=1)
        plt.colorbar()
        plt.savefig(os.path.join(self.dmd_data_path, f'{plot_name}.png'))
    
    def _build_message(self, data_length=2, command_type=0, row=0, column=0, data=None):
        """Function to build messages for the DMD controller. 
        
        Parameters
        ----------
        data_length : int
            How many bits the message consists of.
        command_type : int
            What kind of command we send, 1-7. Notes follows.
        row : int
        column : int
            The place where the command update starts columnwise.
            The row we're updating or where we're starting to update.
        data : np.array
            The values to set for the row at hand or the number of rows to
            fill. (Defaults to None for start/end messages.)

        Returns
        -------
        message : str
            Str of hex code that represents a correct message to the
            controller.

        Notes
        -----
        Sample message :00200000000020C0 [CR]
        : 002 0 0000 00 0020 C0 [CR]
        [colon start of command] [packet with 2 8b words] 
        [default character / display type] [row address] [ column address]
        [data] [checksum] [end character]
        (This is the start and set default command.)

        Message types :
        - 0: default for unspecified values 
        - 1: write a single row
        - 2: fill row with default
        - 3: fill row with copy of last data
        - 4-6: reserved 
        - 7: end transmission / refresh display
        """
        
        def convert_int_to_n_hex(integer, length):
            """ Convenience function to convert an integer to some number of
            bytes."""
            
            # Gives us something like 0x14 (but could be 0xNNNN --> 0xN)
            hex_convert = hex(integer)
            
            # Taking only the numerical characters
            numerical = hex_convert.split('x')[-1]
            
            # Pad with zeros so shorter ints still are the right length
            padded_hex = length*'0' + numerical
            hex_int = padded_hex[-1*length:]

            return hex_int
        
        # Start character
        message = ':'
        # Data length
        message += convert_int_to_n_hex(data_length, 3)
        # Message type
        message += convert_int_to_n_hex(command_type, 1)
        # Row address 
        message += convert_int_to_n_hex(row, 4)
        # Column address
        message += convert_int_to_n_hex(column, 2)
        # Add 00 data for defaults or calculate row hex
        
        # No data for update display command
        if data is None:
            data_hex = ''

        # Single int data for default set or set n rows command
        elif type(data) == int:
            data_hex = convert_int_to_n_hex(data, data_length*2)
        
        # Otherwise we'll have an array of of bits to convert to bytes to send
        # to the controller to set a single row
        else:
            data_hex = ''

            # Convert 8 bits at a time into bytes
            for byte_index in np.arange(0, len(data), 8):
                byte = self._calculate_byte(data[byte_index:byte_index+8])
                data_hex += byte
        
        message += data_hex
        
        # Checksum 
        checksum_int = self._calculate_checksum(message)[0]
        message += convert_int_to_n_hex(checksum_int, 2)
        
        # Add end character
        message = message.upper() + '\n' 
        
        return message
    
    def _calculate_byte(self, hex_array):
        """ Calculates a byte from 8 hex bits.

        Parameters
        ----------
        hex_array : np.array 
            Array of 8 1s or 0s.

        Returns
        -------
        byte : str
            Str of hex.
        """

        if len(hex_array) != 8:
            raise IndexError("Hex array is the wrong size.")
        
        hex_array = np.array(np.array(hex_array, dtype=int), dtype='str')
        bit_sum = ''
        for bit in hex_array:
            # Reverse the order of the bits
            bit_sum = bit + bit_sum
        int_value = int(bit_sum, 2)
        hex_value = hex(int_value)
        
        # Pad in case it's a one digit
        hex_value = '00' + hex_value.split('x')[-1]
        byte = hex_value[-2:]

        return byte
    
    def _calculate_checksum(self, str_byte_message): 
        
        """  Calculates the checksum for a message. 
         
        Parameters 
        ---------- 
        str_byte_message : str
            Str message of hex bytes. 
        
        Returns 
        ------- 
        checksum : tuple 
            The checksum in int and str of hex form. 
        
        Notes
        -----
        # 0x00 + 0x20 + 0x00 + 0x00 + 0x00 + 0x00 + 0x20 = 0x0040 = 0x40
        # 0xFF - 0x40 = 0xC0 
        # to verify :00200000000020C0 [CR]
        # 0x00 + 0x20 + 0x00 + 0x00 + 0x00 + 0x20 + 0xC0 = 0x0100 + 0x00 = 0
        
        """
        if str_byte_message[0] == ':':
            str_byte_message = str_byte_message[1:]
        
        # Split the str message into bits
        byte_list = [f'0x{str_byte_message[n:n+2]}' for n in np.arange(0, len(str_byte_message), 2)] 
        byte_sum = 0 
        
        for byte in byte_list: 
            # convert the bit into an integer
            byte_sum += int(byte, 16) 

        # Pull the least significant bit
        byte_digits = hex(byte_sum).split('x')[-1][-2:] 

        # Calculate the two's complement 
        checksum = int('0xff', 16) - int(f'0x{byte_digits}', 16) + 1 
        
        return checksum, hex(checksum)

    def load_RADEC_list(self):
        pass

    def convert_RADEC_to_pixels(self):
        pass
        
    def convert_pixels_to_DMDs(self):
        pass

    def create_DMD_shape(self):
        pass

    def load_DMD_shape(self):
        pass

    
    def do_nothing(self):
        pass
 