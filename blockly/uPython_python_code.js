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
  var code = '...\n';
  return code;
};

Blockly.Python['neopixel_set_pixel'] = function(block) {
  var number_pixel_number = block.getFieldValue('pixel_number');
  var colour_colour = block.getFieldValue('colour');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['neopixel_set_all'] = function(block) {
  var colour_colour = block.getFieldValue('colour');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['neopixel_animation'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['motor'] = function(block) {
  var number_name = block.getFieldValue('NAME');
  var dropdown_intensity = block.getFieldValue('intensity');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['speaker'] = function(block) {
  var number_pin_number = block.getFieldValue('pin_number');
  var dropdown_freq = block.getFieldValue('freq');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['temp_declare'] = function(block) {
  var number_pin_num = block.getFieldValue('pin_num');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['temp_print'] = function(block) {
  var number_pin_num = block.getFieldValue('pin_num');
  // TODO: Assemble Python into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['import_modules'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = 'import time, machine, onewire, ds18x20, neopixel, network, esp, utime\n';
  return code;
};