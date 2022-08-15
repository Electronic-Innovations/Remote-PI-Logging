


class TestreadEDM(unittest.TestCase):
    
    def setUp(self):
        self.EDM =EDMSerial()
    
    def test_wrong_port(self):
        with self.assertRaises(SystemExit) as output:
            self.EDM.getEDMdata('unitttest_wrongport.txt')
        self.assertEqual(output.exception.code,-2)
        
    # This will change depending on system, on RPi will get -2 on mac recives -1 expection
    def test_port_is_open(self):
        self.EDM.changePort('/dev/cu.usbserial-240')
        com = serial.Serial()
        com.baudrate = 57600
        com.port = self.EDM.port
        #com.port = '/dev/ttyUSB0'
        com.exclusive = True
        com.timeout = 180
        com.xonxoff = True
        com.open()
        self.EDM.changePort('/dev/cu.usbserial-240')
        with self.assertRaises(SystemExit) as output:
            self.EDM.getEDMdata('unitttest_openport.txt')
        self.assertEqual(output.exception.code,-2)
        com.close()
        
        
        
    def test_file_is_created(self):
        self.EDM.changePort('/dev/cu.usbserial-240')
        with self.assertRaises(SystemExit) as output:
            self.EDM.getEDMdata('create_new_text_test.txt')
            self.assertTrue(os.path.isfile('create_new_text_test.txt'))
        self.assertEqual(output.exception.code,1)
        os.remove('create_new_text_test.txt')
    
    def test_data_recieved(self):
        self.EDM.changePort('/dev/cu.usbserial-240')
        self.EDM.getEDMdata('size_test.txt')
        self.assertGreater(os.path.getsize('size_test.txt'),200000)
        os.remove('size_test.txt')
unittest.main()
