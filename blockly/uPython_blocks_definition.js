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

Blockly.Blocks['switch_led'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["Zapni","1"], ["Vypni","0"]]), "drop")
        .appendField("LEDku na Pine")
        .appendField(new Blockly.FieldNumber(0, 0, 16), "pin_number");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['sleep_ms'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Počkaj")
        .appendField(new Blockly.FieldNumber(0, 0), "time_value")
        .appendField("milisekúnd");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(345);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['button_input'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("je tlačidlo na Pine")
        .appendField(new Blockly.FieldNumber(0, 0), "pin_number")
        .appendField(new Blockly.FieldDropdown([["stlačené","1"], ["nestlačené","0"]]), "NAME");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['neopixel_declare'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Pripoj NeoPixel pásik na Pin číslo")
        .appendField(new Blockly.FieldNumber(0, 0), "pin_num");
    this.appendDummyInput()
        .appendField("s dĺžkou")
        .appendField(new Blockly.FieldNumber(8, 0), "pixels")
        .appendField("pixelov");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['neopixel_set_pixel'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Zmeň Pixel číslo")
        .appendField(new Blockly.FieldNumber(1, 1), "pixel_number")
        .appendField("na")
        .appendField(new Blockly.FieldColour("#ff0000"), "colour")
        .appendField("farbu");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['neopixel_set_all'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Zmeň všetky Pixely na")
        .appendField(new Blockly.FieldColour("#ff0000"), "colour")
        .appendField("farbu");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['neopixel_animation'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Prehraj NeoPixel animáciu:")
        .appendField(new Blockly.FieldDropdown([["Prelet","prelet"], ["Výstraha","vystraha"], ["Spiatočný prelet","rev_prelet"]]), "NAME");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['motor'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Na Pine číslo")
        .appendField(new Blockly.FieldNumber(0), "NAME")
        .appendField("vibruj motorom na")
        .appendField(new Blockly.FieldDropdown([["100%","255"], ["80%","204"], ["60%","153"], ["40%","102"], ["20%","51"], ["0%","0"]]), "intensity")
        .appendField("percent");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['speaker'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Na Pine číslo")
        .appendField(new Blockly.FieldNumber(0, 0), "pin_number")
        .appendField("bzuč frekvenciou")
        .appendField(new Blockly.FieldDropdown([["1000","1000"], ["900","900"], ["800","800"], ["700","700"], ["600","600"], ["500","500"], ["400","400"], ["300","300"], ["200","200"], ["100","100"], ["0","0"]]), "freq")
        .appendField("Hz");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['temp_declare'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Pripoj Teplomer na Pin číslo")
        .appendField(new Blockly.FieldNumber(0, 0), "pin_num");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['temp_print'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Odmeraj teplotu na Pine číslo")
        .appendField(new Blockly.FieldNumber(0, 0), "pin_num");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

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

Blockly.Blocks['import_modules'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Zapni Hardvér");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(255);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};