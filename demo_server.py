import argparse
import falcon
from hparams import hparams, hparams_debug_string
import os
from synthesizer import Synthesizer


html_body = '''<html>
  <title>Demo</title>
  <style>
    *,p{
        margin: 0;
    }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      font-size: 14px;
      color: #f2f2f2;
      padding: 0;
      margin: 0;
      background-color: #1f1f1f;
    }
    input {
      font-size: 14px;
      padding: 8px 12px;
      outline: none;
      border: 1px solid #ddd;
    }
    input:focus {
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
    }
    p {
      padding: 5px;
    }
    button {
      background: rgb(91, 91, 91);
      padding: 9px 14px;
      margin-left: 8px;
      border: none;
      outline: none;
      color: #fff;
      font-size: 14px;
      border-radius: 4px;
      cursor: pointer;
      border: 1px solid white;
    }
    button:hover {
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
      opacity: 0.9;
    }
    button:active {
      background: #29f;
    }
    button[disabled] {
      opacity: 0.4;
      cursor: default;
    }
    .hero{
        min-height: 300px;
        background:linear-gradient(to right,rgb(4, 34, 74),rgb(29, 29, 66));
        margin-bottom: 12px;

    }
    .text-white{
        color: white;
    }
    .p-2{
        padding: 1rem;
    }
    .weight-400{
        font-weight: 400;
    }
    .d-flex{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .text-size-40{
        font-size: 60px;
    }
    .left{
        max-width: 600px;
        text-align: center;
        padding: 10px 30px;
    }
    .mx-auto{
        max-width: 900px;
        margin: 10px auto;
    }
    .mb{
      margin-bottom: 40px;
    }
    .abstract{
        font-size: 16px;
        line-height: 25px;
        font-weight: 400px;
        text-align: justify ;
    }
    .waveform {
        max-width: 600px;
        width: 100%;
        height: 300px;
        position: relative;
        overflow: hidden;
        padding: 0px 10px;
        margin-left: 10px;
    }
    .waveform .bar {
        position: absolute;
        bottom: 0;
        width: 1px;
        background-color: #71b5fe;
        animation: slide 4s alternate infinite ;
    }
    @keyframes slide {
        0%{
          transform: translateX(0);
          background-color: rgb(0, 242, 255);
        }
        50%{
            background-color: rgb(170, 0, 255);
        }
        100%{
            background-color: rgb(90, 128, 0);
            transform: translateX(100%);
        }
        
    }
  </style>
    <div
    class="hero d-flex"
    >
    <!-- <div class="waveform" id="waveform">
    </div> -->
    <div class="left">
      <h1 class="text-white weight-400 text-size-40">Infusing Emotion To Text-To-Speech</h1>
      <div>
        <p>Authors</p>
        <p style="font-size: 18px; font-weight: 400;">AbdulRahman, Rupesh Yadav, Sudip Thapa and Yared Alemeyehu</p>
      </div>
    </div>
    </div>
    <div class="mx-auto abstract">
        <h4>Abstract</h4>
        Current state-of-the-art Text-To-Speech (TTS) models excel in generating high-quality speech. 
        However, they often lack the ability to convey emotions effectively, resulting in a robotic or 
        mechanical tone. In this paper, we propose a solution to address this limitation. Our approach 
        involves enhancing the mel-spectrogram output from pre-trained models Tacotron, Fastspeech2
        with emotion vectors extracted from expressive speech samples. By leveraging end-to-end 
        neural architectures, our goal is to develop an emotional speech synthesizer capable of infusing 
        synthesized speech with emotional expressions. This entails modifying existing TTS 
        frameworks to accept emotion vectors alongside textual input, thereby enabling the synthesis 
        of emotionally rich speech output. Through this research initiative, we aspire to make 
        significant strides in the field of TTS synthesis, ultimately enhancing the quality and naturalness 
        of human-computer interactions.
    </div>
    <form class="p-2 mx-auto">
      <input id="text" type="text" size="40" placeholder="Enter Text" />
      <div style="display: flex; gap: 10px;align-items: center; margin-top: 20px;">
      <input type="radio" value="happy" name="emotion" id="happy" />
      <label for="happy">Happy</label>
    </div>
    <div style="display: flex; gap: 10px;align-items: center;">
      <input type="radio" value="sad" name="emotion" id="sad" />
      <label for="sad">Sad</label>
    </div>
    <div style="display: flex; gap: 10px;align-items: center;">
      <input type="radio" value="neutral" name="emotion" id="neutral"/>
      <label for="neutral">neutral</label>
    </div>
      <button id="button" name="synthesize" style="margin-top: 20px;">Synthesis</button>
    </form>
    <div class="mx-auto">
    <p id="message" ></p>
    <audio id="audio" class="mx-auto" controls autoplay hidden></audio>
    </div>
    <div class="mx-auto mb">
        <h3>Model architecture</h3>
        <img src="/image" alt="model" height="700px" width="100%" />
    </div>
    <script>
      function q(selector) {
        return document.querySelector(selector);
      }
      q("#text").focus();
      q("#button").addEventListener("click", function (e) {
        text = q("#text").value.trim();
        if (text) {
          q("#message").textContent = "Synthesizing...";
          q("#button").disabled = true;
          q("#audio").hidden = true;
          synthesize(text);
        }
        e.preventDefault();
        return false;
      });
      function synthesize(text) {
        fetch("/synthesize?text=" + encodeURIComponent(text), {
          cache: "no-cache",
        })
          .then(function (res) {
            if (!res.ok) throw Error(res.statusText);
            return res.blob();
          })
          .then(function (blob) {
            q("#message").textContent = "";
            q("#button").disabled = false;
            q("#audio").src = URL.createObjectURL(blob);
            q("#audio").hidden = false;
          })
          .catch(function (err) {
            q("#message").textContent = "Error: " + err.message;
            q("#button").disabled = false;
          });
      }
    </script>
    <script>
        // Generate random data for the sound wave
        const data = [];
        for (let i = 0; i < 1000; i++) {
            data.push(Math.random());
        }
    
        // Render the sound wave
        const waveform = document.getElementById('waveform');
        for (let i = 0; i < data.length; i++) {
            const bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.height = (data[i] * 100) + '%';
            bar.style.left = (i * 2) + 'px'; // Adjust width based on the number of data points
            waveform.appendChild(bar);
        }
    </script>
  </body>
</html>

'''


class UIResource:
  def on_get(self, req, res):
    res.content_type = 'text/html'
    res.body = html_body


class SynthesisResource:
  def on_get(self, req, res):
    if not req.params.get('text'):
      raise falcon.HTTPBadRequest()
    res.data = synthesizer.synthesize(req.params.get('text'))
    res.content_type = 'audio/wav'

class ImageResource:
    def on_get(self, req, resp):
        # Open the image file and read its content
        with open('model_emotional_tts.png', 'rb') as image_file:
            resp.content_type = 'image/png'  # Set the content type
            resp.body = image_file.read()    # Set the body of the response

synthesizer = Synthesizer()
api = falcon.API()
api.add_route('/synthesize', SynthesisResource())
api.add_route('/', UIResource())
api.add_route('/image', ImageResource())


if __name__ == '__main__':
  from wsgiref import simple_server
  parser = argparse.ArgumentParser()
  parser.add_argument('--checkpoint', required=True, help='Full path to model checkpoint')
  parser.add_argument('--port', type=int, default=9000)
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  args = parser.parse_args()
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  hparams.parse(args.hparams)
  print(hparams_debug_string())
  synthesizer.load(args.checkpoint)
  print('Serving on port %d' % args.port)
  simple_server.make_server('0.0.0.0', args.port, api).serve_forever()
else:
  synthesizer.load(os.environ['CHECKPOINT'])
