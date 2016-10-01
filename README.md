# Cat feeder

You have a cat. The cat eats only fish, milk and bread. If he is hungry and you feed him, you get an email alert that the cat is full and content. If more than 15 minutes pass and he hasn't eaten, you receive an email alert that kindly reminds you to feed him. After all, he *is* your cat.

**On the serious side:**

To feed the cat, upload an image file to an S3 bucket. Upon upload, an AWS Lambda function downloads the image, sends it to Google Cloud Vision for some image analysis. If the image contains fish, bread or milk - the "cat" eats.

Meanwhile, another AWS Lambda function runs every minute to check if the cat turned hungry again. Email alerts are sent only once at state transition.


## Making this work on your computer\AWS resources
Bucket and file names are self-evident in the code - change them to resources that you own if you want this to work for you. Also, in `timed_state_checker.py`, you'll have to configure the AWS SES interface to use resources that you own, so email alerts would be sent. Don't forget to set the triggers for your Lambda function to act on `put` events for the specific S3 bucket that you use, and for the file types that you intend to upload.

Zip up everything (including a credentials file that `upload_handler.py` uses to connect to Google Cloud Vision) and upload it to an AWS Lambda function. Create another AWS Lambda function and just paste the adjusted contents of `timed_state_checker.py`.

## License

The MIT License (MIT)

Copyright (c) 2016 Asaf Chelouche

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
