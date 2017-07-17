Blockly.Python['sleep'] = function(block) {
  var number_sleep_time = block.getFieldValue('sleep_time');
  // TODO: Assemble Python into code variable.
  var code = 'time.sleep(' + number_sleep_time + ')\n';
  return code;
};

Blockly.Python['switch_led'] = function(block) {
  var dropdown_drop = block.getFieldValue('drop');
  var number_pin_number = block.getFieldValue('pin_number');
  // TODO: Assemble Python into code variable.
  var code = 'machine.Pin(' + number_pin_number + ', machine.Pin.OUT).value(' + dropdown_drop + ')\n';
  return code;
};

Blockly.Python['sleep_ms'] = function(block) {
  var number_time_value = block.getFieldValue('time_value');
  // TODO: Assemble Python into code variable.
  var code = 'utime.sleep_ms(' + number_time_value + ')\n';
  return code;
};

Blockly.Python['button_input'] = function(block) {
  var number_pin_number = block.getFieldValue('pin_number');
  var dropdown_name = block.getFieldValue('NAME');
  // TODO: Assemble Python into code variable.
  var code = 'machine.Pin(' + number_pin_number + ', machine.Pin.IN).value() == ' + dropdown_name;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['neopixel_declare'] = function(block) {
  var number_pin_num = block.getFieldValue('pin_num');
  var number_pixels = block.getFieldValue('pixels');
  // TODO: Assemble Python into code variable.
  var code = 'np = neopixel.NeoPixel(machine.Pin(' + number_pin_num + '), ' + number_pixels + ')\n';
  return code;
};

Blockly.Python['neopixel_set_pixel'] = function(block) {
  var number_pixel_number = block.getFieldValue('pixel_number');
  var colour_colour = block.getFieldValue('colour');
  // TODO: Assemble Python into code variable.
  var code = 'np[' + number_pixel_number + '-1] = (int("'+colour_colour+'"[1:3], 16), int("'+colour_colour+'"[3:5], 16), int("'+colour_colour+'"[5:7], 16))\nnp.write()\n';
  return code;
};

Blockly.Python['neopixel_set_all'] = function(block) {
  var colour_colour = block.getFieldValue('colour');
  // TODO: Assemble Python into code variable.
  var code = 'for i in range(np.n): np[i] = (int("'+colour_colour+'"[1:3], 16), int("'+colour_colour+'"[3:5], 16), int("'+colour_colour+'"[5:7], 16))\nnp.write()\n';
  return code;
};

Blockly.Python['neopixel_animation'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  // TODO: Assemble Python into code variable.
  var code = 'n = np.n\n\
def prelet():\n\
  for j in range(n):\n\
    for i in range(n):\n\
      np[i] = (0, 0, 0)\n\
    np[j] = (255, 255, 255)\n\
    np.write()\n\
    time.sleep_ms(50)\n\
def rev_prelet():\n\
  for j in range(n-1, -1, -1):\n\
    for i in range(n):\n\
      np[i] = (0, 0, 0)\n\
    np[j] = (255, 255, 255)\n\
    np.write()\n\
    time.sleep_ms(50)\n\
def vystraha():\n\
  for i in range(0, 4 * 256, 8):\n\
    for j in range(n):\n\
      if (i // 256) % 2 == 0:\n\
        val = i & 0xff\n\
      else:\n\
        val = 255 - (i & 0xff)\n\
      np[j] = (val, 0, 0)\n\
    np.write()\n\
' + dropdown_name + '()\n';

  return code;
};

Blockly.Python['motor'] = function(block) {
  var number_name = block.getFieldValue('NAME');
  var dropdown_intensity = block.getFieldValue('intensity');
  // TODO: Assemble Python into code variable.
  var code = 'machine.PWM(machine.Pin('+number_name+'), freq=500, duty='+dropdown_intensity+'*4)\n';
  return code;
};

Blockly.Python['speaker'] = function(block) {
  var number_pin_number = block.getFieldValue('pin_number');
  var dropdown_freq = block.getFieldValue('freq');
  // TODO: Assemble Python into code variable.
  var code = 'machine.PWM(machine.Pin('+number_pin_number+'), freq='+dropdown_freq+', duty=512)\n';
  return code;
};

Blockly.Python['temp_declare'] = function(block) {
  var number_pin_num = block.getFieldValue('pin_num');
  // TODO: Assemble Python into code variable.
  var code = 'temp_pin = ds18x20.DS18X20(onewire.OneWire(machine.Pin('+number_pin_num+')))\n\
temp_address = temp_pin.scan()[0]\n\
def get_temp(temp_address):\n\
  temp_pin.convert_temp()\n\
  time.sleep_ms(750)\n\
  return temp_pin.read_temp(temp_address)\n';
  return code;
};

Blockly.Python['temp_print'] = function(block) {
  var number_pin_num = block.getFieldValue('pin_num');
  // TODO: Assemble Python into code variable.
  var code = 'get_temp(temp_address)';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['import_modules'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = 'import time, machine, onewire, ds18x20, neopixel, network, esp, utime\n';
  return code;
};