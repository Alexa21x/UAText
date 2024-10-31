# UAText
UAText is a simple tool designed to aid in modding and editing localization text for games based on *Unreal Engine 4/5* that use the .uasset format for localization files.

This project began due to the lack of tools available for editing localization files in .uasset format, which differs from the more commonly used locres format. With UAText, users can open and edit .uasset localization files, making the localization modding process more accessible.

Currently, UAText supports the game Evil Nun The Broken Mask. Future updates aim to expand support to other *Unreal Engine* games that also use the .uasset format for localization.

## Usage
1. Place the Localization File
Copy the .uasset localization file you want to edit into the same directory as UAText.exe.

2. Decode the Localization File
Run the following command to decode the file:

```bash
UAText.exe -decode
```
This command will generate a new file with the _decode.txt suffix, which you can open and edit as needed.

3. Edit the Decoded File
Open the _decode.txt file and make the necessary edits to the localization text.

4. Encode the Edited File
After editing, run the following command to convert the file back to .uasset format:

```bash
UAText.exe -encode
```
This will create a new file with the _NEW.uasset suffix, representing the edited localization file in .uasset format.

## Contributing
I welcome all forms of contributions and support from the modding community to enhance UAText’s functionality and expand its support for other Unreal Engine games. Feel free to submit improvements, report issues, and make feature requests to help make this tool even better. Your input is invaluable for the continued development of UAText.

## License
This project is licensed under the GNU General Public License v3.0 (GPL-3.0). You are free to modify, distribute, and use this software under the terms of this license. See the LICENSE.md file for details.
