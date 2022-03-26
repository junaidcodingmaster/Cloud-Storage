import pyfiglet
import filesUploader

from simple_chalk import chalk

# On start up
td = filesUploader.TransferData

if td.token() == "none":
    td.token()

else:
    pass

td.clear()

# Logo
rawLogo = pyfiglet.figlet_format("Cloud")
colorLogo = chalk.bold.green(rawLogo)
rawSideLogo = pyfiglet.figlet_format("Storage")
colorSideLogo = chalk.bold.blue(rawSideLogo)
logo = colorLogo + colorSideLogo

# Display
print(logo)  # This will display Logo

# Our module
td()
# For Copyright
td.copyright()
