#!/usr/bin/python3
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string(clear, 1)
mylcd.lcd_display_string(clear, 2)
mylcd.lcd_display_string(clear, 3)
mylcd.lcd_display_string('No connection!', 1)
mylcd.lcd_clear()
