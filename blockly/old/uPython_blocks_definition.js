Blockly.Blocks['import_machine'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Povoľ Používanie Pinov");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(255);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['pin_object'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Pin číslo")
        .appendField(new Blockly.FieldNumber(0, 0, 100, 1), "pin");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['set_pin_output'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Nastav")
        .appendField(new Blockly.FieldVariable("item"), "pin_object")
        .appendField("na hodnotu")
        .appendField(new Blockly.FieldDropdown([["1","1"], ["0","0"]]), "value");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['sleep'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Počkaj")
        .appendField(new Blockly.FieldNumber(0, 0), "sleep_time")
        .appendField("sekúnd");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};