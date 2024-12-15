<a id="readme-top"></a>
<!-- *** Don't forget to give the project a star! -->

<!-- PROJECT SHIELDS -->
<div align="center">

[![Releases][release-shield]][release-url]
[![Builds][build-shield]][build-url]
[![Commits][commits-shield]][commits-url]
[![Stars][stars-shield]][stars-url]
[![License][license-shield]][license-url]
[![Issues][issues-shield]][issues-url]
[![Pulls][pulls-shield]][pulls-url]

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/logo.png" alt="Logo" width="auto" height="100">

  <h3 align="center">Vimar By-me Plus for HomeAssistant</h3>

  <p align="center">
    <p>An Home Assistant Custom Integration for Vimar Gateway 01410/01411<p/>
    <p>If you like this repo, give me a ⭐ clicking on the `Star` button in upper right corner<p/>
    <a href="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/issues/new?labels=bug&template=bug-report.md">Report Bug</a>
    ·
    <a href="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/issues/new?labels=enhancement&template=feature-request.md">Request Feature</a>
  </p>
    <br />
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#support">Support</a></li>
    <li><a href="#requirements">Requirements</a></li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#step-13-home-assistant---install-component">[Step 1/3] Home Assistant - Install Component</a></li>
        <li><a href="#step-23-vimar-pro---initial-setup">[Step 2/3] Vimar Pro - Initial Setup</a></li>
        <li><a href="#step-33-vimar-pro---generate-setup-code">[Step 3/3] Vimar Pro - Generate Setup Code</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#debugging">Debugging</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

This integration uses the Web Socket protocol to communicate with the Vimar Gateway and integrate in Home Assistant all elements found on the plant.
The component follows the Vimar Official integration process and provides an interface that can be used to read the states and to send commands to the managed devices, in a similar way to what is possible using the Vimar VIEW application. The interface is usable only in the local network where the By-me home automation Gateway is configured and is based on a proprietary IP Connector protocol.

Further information here: [Vimar Official Website][vimar-integration-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Support 

Hey there! I'm a tech enthusiast and dedicated coder, fuelled by caffeine and a passion for the home-automation world.
Your support directly powers my coffee stash, keeps my energy up, and lets me focus more on creating and maintaining the resources you rely on.

If my work has helped you in any way, consider buying me a coffee — it’s a small way to contribute but makes a big difference and helps keep this project alive and maintained. 
Thank you for fueling my passion for tech and open-source! ❤️

<a href="https://www.buymeacoffee.com/andreaprosseda">
  <img align="center" src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="coffee image" height="55" />
</a>

<a href="https://paypal.me/AndreaProsseda">
  <img align="center" src="https://villageatithaca.org/wp-content/uploads/2020/03/paypal-donate-button.png" alt="paypal image" height="80" />
</a>


<!-- Requirements -->
## Requirements

* Vimar Gateway:
  - 01410 - By-me home automation Light Gateway
  - 01411 - By-me home automation Gateway
* Vimar Components (at least one):
  - Access
  - Audio
  - Clima
  - Energy
  - Irrigation
  - Light
  - Sensor
  - Switch
  - Shutter
* Vimar Pro app access (credentials)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Installation -->
## Installation

The installation phase is divided in three steps:
* [Step 1/3] Home Assistant - Install Component
* [Step 2/3] Vimar Pro - Initial Setup
* [Step 3/3] Vimar Pro - Generate Setup Code

N.B. Steps 1 and 2 are needed only the first time, while the third one is required everytime the integration is reinstalled or cleaned

### [Step 1/3] Home Assistant - Install Component

#### Method 1: [HACS][hacs-url]
:warning: This component has not yet been approved by HACS and is not yet direclty visible, steps 2-5 are required at the moment.
> 1. Open HACS
> 2. Click on the three dots (in the top right corner)
> 3. Select Custom Repositories (Archivi digitali personalizzati)
> 4. Copy `https://github.com/andreaprosseda/vimar-byme-plus-homeassistant` as Repository and Type as `Integration`
> 5. Add Custom Repository
> 5. Search now for `Vimar By-me Plus HUB` in HACS
> 6. Click the blue download in the right bottom side
> 7. Restart Home Assistant

#### Method 2: Manual
> 1. Download the latest release from `GitHub`
> 2. Copy `vimar_by_me_plus` (custom_components/vimar_byme_plus) 
> 3. Paste it in `custom_components` folder in your Home Assistant config folder
> 3. Restart Home Assistant

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### [Step 2/3] Vimar Pro - Initial Setup

The insertion of the public key in the By-me Gateway is required to enable the communication between this integration and the Gateway.

<details>
  <summary>Why?</summary>
For security reasons, it is required that the client using the integration interface is identified and authenticated by the By-me home automation Gateway. 

For this purpose, an asymmetric encryption mechanism is used which requires the client to encrypt the access credentials to the server using its private key, while the server verifies the correctness of the credentials and the identity of the client using the public key (which must be previously inserted into the By-me home automation Gateway).
</details>

<br/>

Here the steps to follow:
steps:
1. Open Vimar Pro app
2. Click on the plant name
3. Click on `i` on the right of the Gateway name
4. Click on 
   * `Device Maintenance`
   * `Third Party Client Management`
   * `Associate New Client`
   * `Add Integration`
5. Fill the `identifier` field with `xm7r1`
6. Click on `Add`

<div align="center">
    <img src="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/vimar_pro_first_setup.gif" alt="Gif" width="200">
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### [Step 3/3] Vimar Pro - Generate Setup Code

Here the steps to follow to generate a Setup Code, needed for the integration phase on HomeAssistant (see <a href="#usage">Usage</a>):
1. Open Vimar Pro app
2. Click on the plant name
3. Click on `i` on the right of the Gateway name
4. Click on 
   * `Device Maintenance`
   * `Third Party Client Management`
   * `Associate New Client`
5. Fill the `Name` field with a name you prefer
6. Select `Vimar By-me Plus HomeAssistant` from the integration list (if not available <a href="#step-23-vimar-pro---initial-setup">add it</a>)
7. Click on `Generate Setup Code`
8. Save `Setup Code`
9. Click on this [link](https://vimar-byme-plus-authenticator.onrender.com/api/vimar/identifier) to awake the Authenticator Backend and wait for its response. (It may take up to 5 minutes!)

<details>
  <summary>Why Step 9?</summary>
The Authenticator Backend is deployed on a Free Instance and it is spin down after 15 minutes of inactivity, causing delays upon reactivation. Opening the link leads to the reactivation of the Backend and speeds up the next phase.

N.B. The Backend is invoked only for the Setup Phase and not during the operational phase.
</details>

<br/>

:warning: `Setup Code` expires in few minutes, create a new one if it doesn't work

<div align="center">
    <img src="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/vimar_pro_setup_code.gif" alt="Gif" width="200">
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage
It's almost done! Let's proceed to integrate the custom component on Home Assistant:
1. Open Home Assistant
2. Click on `Settings`
3. The Gateway will be automatically discovered and ready to configure
4. Click on `Configure`
5. Fill `Setup Code` with the one you created in the previous step
6. Wait for the integration

:warning: This process may take up to 5 minutes. Be patient and wait for the process to be completed!

![Usage Tutorial][usage-tutorial]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Debugging
To enable debug add this link on your Home Assistant config YAML:

```yaml
logger:
  default: info
  logs:
    custom_components.vimar_byme_plus: debug
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Add direct integration with Vimar Gateway 01410/01411
- [x] Add Access
  - [x] Gate
  - [x] DoorWindow
- [X] Add Audio
  - [x] Zone
  - [X] RadioFM
  - [X] RCA
  - [X] Bluetooth (not tested)
- [X] Add Automation
  - [X] On Off
  - [X] Technical Alarm
- [X] Add Clima
  - [x] Clima Zone
- [x] Add Energy
  - [x] Energy Load
  - [x] Energy Measure (1P & 3P)
  - [x] Energy Load Control (1P & 3P)
  - [x] Energy Load Control Production (1P & 3P)
- [x] Add Irrigation
  - [x] Multi Zone
- [x] Add Light
  - [x] Switch (On/Off)
  - [x] Dimmer (Brightness)
- [x] Add Scene
  - [x] Scene Executor
- [x] Add Sensor
  - [x] Air Quality Gradient
  - [x] Humidity
  - [x] Interface Contact
  - [x] Weather Station
- [X] Add Shutter
  - [x] Shutter with Position
  - [x] Shutter without Position
  - [x] Shutter Slat with Position
  - [x] Shutter Slat without Position
  - [x] Curtain with Position
  - [x] Curtain without Position
- [x] Code and Readme cleaning
- [ ] Add not implemented types of:
  - [ ] Audio (Bluetooth)
  - [ ] Clima (Mitsubishi, Daikin, LG, etc)
  - [ ] Light (RGB, Philips, etc)
- [ ] Add Alarm
- [ ] Add Video Intercom/Door Bell

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

#### Current Contributors:

<a href="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=andreaprosseda/vimar-byme-plus-homeassistant" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!
<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
[release-shield]: https://img.shields.io/github/v/release/andreaprosseda/vimar-byme-plus-homeassistant?include_prereleases&style=for-the-badge
[release-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/releases

[commits-shield]: https://img.shields.io/github/commit-activity/t/andreaprosseda/vimar-byme-plus-homeassistant?style=for-the-badge
[commits-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/commits/main/

[build-shield]: https://img.shields.io/github/actions/workflow/status/andreaprosseda/vimar-byme-plus-homeassistant/validate.yml?style=for-the-badge
[build-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/actions/workflows/validate.yml

[issues-shield]: https://img.shields.io/github/issues/andreaprosseda/vimar-byme-plus-homeassistant?style=for-the-badge
[issues-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/issues

[pulls-shield]: https://img.shields.io/github/issues-pr/andreaprosseda/vimar-byme-plus-homeassistant?style=for-the-badge
[pulls-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/pulls

[stars-shield]: https://img.shields.io/github/stars/andreaprosseda/vimar-byme-plus-homeassistant?style=for-the-badge
[stars-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/stargazers

[license-shield]: https://img.shields.io/github/license/andreaprosseda/vimar-byme-plus-homeassistant?style=for-the-badge
[license-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/LICENSE

[coffee-shield]: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
[coffee-url]: https://www.buymeacoffee.com/andreaprosseda

[paypal-shield]: https://villageatithaca.org/wp-content/uploads/2020/03/paypal-donate-button.png
[paypal-url]: https://paypal.me/AndreaProsseda

[vimar-integration-url]: https://www.vimar.com/it/it/integrazione-con-il-sistema-domotico-by-me-plus-17577122.html
[hacs-url]: https://hacs.xyz

[product-screenshot]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/screenshot.png
[usage-tutorial]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/usage.gif
