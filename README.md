<a id="readme-top"></a>
<!-- *** Don't forget to give the project a star! -->

<!-- PROJECT SHIELDS -->
<div align="center">

[![Releases][release-shield]][release-url]
[![Commits][commits-shield]][commits-url]
[![Stars][stars-shield]][stars-url]
[![License][license-shield]][license-url]
[![Builds][build-shield]][build-url]
[![Bugs][bugs-shield]][bugs-url]
[![Enhancements][enhancements-shield]][enhancements-url]

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <picture>
    <source srcset="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/logo-on-dark.png" media="(prefers-color-scheme: dark)" width="auto" height="80"/>
    <img src="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/logo-on-light.png" alt="Home Assistant Logo" width="auto" height="80"/>
  </picture>

  <h3 align="center">Vimar By-me Plus for HomeAssistant</h3>

  <p align="center">
    <p>An unofficial Home Assistant Custom Integration for Vimar Gateway 01410/01411<p/>
    <p>If you like this repo, give me a ⭐ clicking on the `Star` button in upper right corner<p/>
    <a href="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/issues/new?labels=bug&template=bug-report.md">Report Bug</a>
    ·
    <a href="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/issues/new?labels=enhancement&template=feature-request.md">Request Feature</a>
  </p>
    <br />
</div>



> [!IMPORTANT]
> This is a personal project developed by me and is not affiliated with, maintained, authorized, or endorsed by Vimar S.p.A. in any way. Use at your own risk.

## Built by Your Support

Hey there! 👋 What started as a fun project has turned into something much bigger! 

This integration has been a truly time-consuming project, requiring many hours of development and a lot of hard work. Every line of code, every test, every bug fix has been carefully crafted to provide the best possible experience.

If my work has been helpful to you, consider making a donation. Every contribution, no matter how small, makes a big difference and allows me to keep dedicating time and resources to maintaining and improving this integration.

<a href="https://paypal.me/AndreaProsseda">
  <img align="center" src="https://villageatithaca.org/wp-content/uploads/2020/03/paypal-donate-button.png" alt="paypal image" height="55" />
</a>

<a href="https://www.buymeacoffee.com/andreaprosseda">
  <img align="center" src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="coffee image" height="55" />
</a>

<br/>
<br/>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#requirements">Requirements</a></li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#step-15-home-assistant---install-integration">[Step 1/5] Home Assistant - Install Integration</a></li>
        <li><a href="#step-25-vimar-view-pro---initial-setup">[Step 2/5] Vimar VIEW PRO - Initial Setup</a></li>
        <li><a href="#step-35-vimar-view-pro---generate-setup-code">[Step 3/5] Vimar VIEW PRO - Generate Setup Code</a></li>
        <li><a href="#step-45-home-assistant---enable-integration">[Step 4/5] Home Assistant - Enable Integration</a></li>
        <li><a href="#step-55-vimar-view---grant-right-permissions">[Step 5/5] Vimar VIEW - Grant Right Permissions</a></li>
      </ul>
    </li>
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
  - Scene
  - Sensor
  - Switch
  - Shutter
* Vimar VIEW PRO app access (credentials)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Installation -->
## Installation
The installation phase is divided in five steps:
* [Step 1/5](#step-15-home-assistant---install-integration) Home Assistant - Install Integration
* [Step 2/5](#step-25-vimar-view-pro---initial-setup) Vimar VIEW PRO - Initial Setup
* [Step 3/5](#step-35-vimar-view-pro---generate-setup-code) Vimar VIEW PRO - Generate Setup Code
* [Step 4/5](#step-45-home-assistant---enable-integration) Home Assistant - Enable Integration
* [Step 5/5](#step-55-vimar-view---grant-right-permissions) Vimar VIEW - Grant Right Permissions

N.B. Steps 1 and 2 are needed only the first time, while others are required everytime the integration is reinstalled or cleaned

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### [Step 1/5] Home Assistant - Install Integration

> [!NOTE]  
> 🚀 Great news! The integration has been <strong>officially approved by HACS</strong>, no need to add it manually anymore! 🎉

[![Add to my Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andreaprosseda&repository=vimar-byme-plus-homeassistant&category=integration)

#### Method 1: [HACS][hacs-url]
> 1. Open HACS
> 5. Search now for `Vimar By-me Plus HUB` in HACS
> 6. Click the blue download in the right bottom side
> 7. Restart Home Assistant


<details>
  <summary>Can't you find the integration on HACS?</summary>
  <br/>
  :warning: This component has been approved by HACS and is directly visible, but your instance may not have been updated.
  Try with the following method:
  <ol>
    <li>Open HACS</li>
    <li>Click on the three dots (in the top right corner)</li>
    <li>Select Custom Repositories (Archivi digitali personalizzati)</li>
    <li>Copy `https://github.com/andreaprosseda/vimar-byme-plus-homeassistant` as Repository and Type as `Integration`</li>
    <li>Add Custom Repository</li>
    <li>Search now for `Vimar By-me Plus HUB` in HACS</li>
    <li>Click the blue download in the right bottom side</li>
    <li>Restart Home Assistant</li>
  </ol>
</details>


#### Method 2: Manual
> 1. Download the latest release from `GitHub`
> 2. Copy `vimar_by_me_plus` (custom_components/vimar_byme_plus) 
> 3. Paste it in `custom_components` folder in your Home Assistant config folder
> 3. Restart Home Assistant

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### [Step 2/5] Vimar VIEW PRO - Initial Setup

The insertion of the public key in the By-me Gateway is required to enable the communication between this integration and the Gateway.

<details>
  <summary>Why?</summary>
For security reasons, it is required that the client using the integration interface is identified and authenticated by the By-me home automation Gateway. 

For this purpose, an asymmetric encryption mechanism is used which requires the client to encrypt the access credentials to the server using its private key, while the server verifies the correctness of the credentials and the identity of the client using the public key (which must be previously inserted into the By-me home automation Gateway).
</details>

<br/>

Here the steps to follow:
steps:
1. Open Vimar VIEW PRO app
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

### [Step 3/5] Vimar VIEW PRO - Generate Setup Code

Here the steps to follow to generate a Setup Code, needed for the integration phase on HomeAssistant (see <a href="#usage">Usage</a>):
1. Open Vimar VIEW PRO app
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

### [Step 4/5] Home Assistant - Enable Integration

It's almost done! Let's proceed to integrate the custom component on Home Assistant:
1. Open Home Assistant
2. Click on `Settings`
3. The Gateway will be automatically discovered and ready to configure
4. Click on `Configure`
5. Fill `Setup Code` with the one you created in the previous step
6. Wait for the integration

:warning: This process may take up to 5 minutes. Be patient and wait for the process to be completed!

![Usage Tutorial][usage-tutorial]

> [!IMPORTANT]
> Some of the implemented entities can produce custom events. For example, the integration fires events related to scenes activation. You can check these events going to Developer Tools > Events and listening to `vimar_byme_plus_event`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### [Step 5/5] Vimar VIEW - Grant Right Permissions
After associating the integration using the Vimar VIEW PRO app, you need to grant the correct access permissions through the Vimar VIEW app

Here the steps to follow:
1. Open the `Vimar VIEW` app on your device (not `View PRO!`).
2. Go to `Settings`
3. Tap on `Users and Permissions`
4. Scroll down to the `Integrations` section: here you’ll find the new integration created during `Step 3/5`
5. Tap on the integration name and enable all permissions for:
   * `Objects` (preferably all, climate mandatory)
   * `Rooms` (as you prefer)
   * `Settings` (preferably all, climate mandatory) 

> [!IMPORTANT]
> Make sure all devices and features you want to control from Home Assistant have the proper permissions enabled. For example, climate devices require these permissions to allow switching between Heat and Cool modes.

<div align="center">
    <img src="https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/blob/main/images/vimar_grant_permissions.gif" alt="Gif" width="200">
</div>

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
  - [x] Dimmer RGB (Brightness + RGB)
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
  - [ ] Light (Philips, etc)
- [ ] ~~Add Alarm~~
- [ ] ~~Add Video Intercom/Door Bell~~

<br/>

> [!IMPORTANT]
> Although the initial roadmap included the support for the Alarm System and the Video Intercom, the official Vimar specifications do not currently allow for their integration. This development is on hold until Vimar provides official support for these features.

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

[build-shield]: https://img.shields.io/github/actions/workflow/status/andreaprosseda/vimar-byme-plus-homeassistant/release.yml?style=for-the-badge
[build-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/actions/workflows/release.yml

[bugs-shield]: https://img.shields.io/github/issues/andreaprosseda/vimar-byme-plus-homeassistant/bug?style=for-the-badge&label=Bugs
[bugs-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug

[enhancements-shield]: https://img.shields.io/github/issues/andreaprosseda/vimar-byme-plus-homeassistant/enhancement?style=for-the-badge&label=Enhancement%20Requests
[enhancements-url]: https://github.com/andreaprosseda/vimar-byme-plus-homeassistant/issues?q=is%3Aissue%20state%3Aopen%20label%3Aenhancement

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
