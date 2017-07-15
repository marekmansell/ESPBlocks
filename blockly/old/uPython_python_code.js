Blockly.Python['import_machine'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = 'import machine\n';
  return code;
};

Blockly.Python['pin_object'] = function(block) {
  var number_pin = block.getFieldValue('pin');
  // TODO: Assemble Python into code variable.
  var code = 'machine.Pin(' + number_pin + ', machine.Pin.OUT)';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['set_pin_output'] = function(block) {
  var variable_pin_object = Blockly.Python.variableDB_.getName(block.getFieldValue('pin_object'), Blockly.Variables.NAME_TYPE);
  var dropdown_value = block.getFieldValue('value');
  // TODO: Assemble Python into code variable.
  var code = variable_pin_object + '.value(' + dropdown_value + ')\n';
  return code;
};

Blockly.Python['sleep'] = function(block) {
  var number_sleep_time = block.getFieldValue('sleep_time');
  // TODO: Assemble Python into code variable.
  var code = 'sleep(' + number_sleep_time + ')\n';
  return code;
};