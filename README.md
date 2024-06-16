<h1 align="center">
  <br>
  <a href="https://github.com/XylenSky/notify-magnet"><img src="https://raw.githubusercontent.com/XylenSky/notify-magnet/main/Notify_Magnet.png" height="350" alt="Notify Magnet" width="700"></a>
  <br>
  Notify Magnet
  <br>
</h1>

<h4 align="center">A Highly Efficient Notification System for Training and Placement Notices.</h4>

<p align="center">
  <a href="https://github.com/binwiederhier/ntfy">
    <img src="https://img.shields.io/badge/NTFY-MFTP-blue" alt="GitHub">
  </a>
  <a href="https://github.com/XylenSky/notify-magnet">
    <img src="https://img.shields.io/github/last-commit/XylenSky/notify-magnet" alt="Last Commit">
  </a>
  <a href="https://github.com/XylenSky/notify-magnet">
    <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2Fxylensky%2Fnotify-magnet.json?color=pink" alt="Say Thanks">
  </a>
  <a href="https://liberapay.com/ntfy">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&style=flat" alt="Donate">
  </a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#known-issues">Known Issues</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

![screenshot](https://raw.githubusercontent.com/XylenSky/notify-magnet/main/howtousepreview.gif)

## Vision

The primary purpose of this service is to expeditiously inform and remind students participating in CDC internship and placement activities about critical CDC notices. Any inappropriate utilization of this service for unethical purposes may result in disciplinary actions.

## Known Issues

- Date formatting issue: Dates like "17/09/2023, 11.59 PM" may be recognized as "17/09/2023, 11.00 PM" due to non-standard formatting.
- Service Restricted to Campus Network: This service can only be accessed within the campus network, and you will not receive notifications when using mobile data.
- Notification Priority: Notification order may depend on priority when a large number of notifications are missed.
- Expiring Attachments: Attachment links have an expiration time; please download them promptly to avoid loss.
- Cache Limits: Notifications are cached for a limited time; if you exceed this limit (while not connected to the campus network), some notifications may not be delivered.
- Allow background running and auto launch for this application; otherwise, notifications will be missed or delayed.
- Cache Deletion Caution: Avoid clearing the app's cache or using phone manager tools, as it may delete downloaded PDFs of existing messages.
- Mobile Apps: The Android and iPhone apps are not developed by us; if some features don't work, it's beyond our control.
- Restrictions: The service provider disclaims any liability for actions or conduct with the intent of interfering with or obstructing the service's functionality through unethical means.
- Official Directive: Official representatives' instructions may lead to service discontinuation, possibly without notice.
- Infrastructure Issues: Power or network infrastructure failures may affect the service.

## Key Features

- Five Priority Levels: Notifications have five priority levels; most are set to the highest priority. Customize ringtones and notification settings (notify even in DND mode) accordingly.
- No data is collected by the mobile app, and the current setup doesn't even include any third party in the loop to send the notification; notifications are sent directly to your phone via Local Area Network.

## Amazing Features

- Scheduled Notifications: Schedule notifications for recognized dates and times, sent 30 minutes before deadlines to ensure you never miss important events.
- Separate Channels: Internship, Placement, and Error notifications are delivered through separate channels, allowing you to subscribe to error notifications for missed updates.

- Cross-Platform: Compatible with Android, iOS.

## How To Use

**For Android and iOS:**

1. Connect to the any of the campus network.
2. Open the application.
3. Click on the "+" to add a topic (internship, placement, error) [case-sensitive] [do not put any spaces].
4. Select "Use Another Server."
5. Enter the current server address: `http://10.105.34.28`
6. Repeat the above steps for error notifications as well.
7. You can directly open this URL in your browser as well to see all the notifications.
8. If you encounter issues, check back here for any updated IP addresses or port numbers.
9. If you're still experiencing issues, please fill out our [issue reporting form](https://forms.gle/B55UbUkG6fv7246i9).

Current address: 
```
http://10.105.34.28
```


> **Note:**
> All the claims about the application may change based on their owner's consent.
> We kindly request users to carefully read and adhere to the aforementioned risks and conditions associated with this service before proceeding with its use.

## Download

You can download the app from the following platforms:
- **Play Store**: [![Google Play](https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Google_Play_Store_badge_EN.svg/126px-Google_Play_Store_badge_EN.svg.png?20220907104002)](https://play.google.com/store/apps/details?id=io.heckel.ntfy&pcampaignid=web_share)
- **App Store**: [![App Store](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Download_on_the_App_Store_Badge.svg/128px-Download_on_the_App_Store_Badge.svg.png)](https://apps.apple.com/in/app/ntfy/id1625396347)

## Join Us

If you are excited about this project, you can contribute or encourage your fellow students to maintain and enhance it, making it even more feature-rich. [Email us](mailto:xylensky@proton.me).

## Credits

This software utilizes the following open-source packages:

- [MFTP](https://github.com/metakgp/mftp)
- [NTFY](https://github.com/binwiederhier/ntfy)

## License

Made with ❤️ for KGP

The project is dual-licensed under the Custom License. To know more, check out the corresponding project licenses used here for more information.
