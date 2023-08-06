import base64
import hashlib
import io
import os

from psd_tools import PSDImage

from psd2html.storage import get_storage


class Reader:

    def _reset(self):
        self._psd = None

    def _set_input(self, input_data):
        if hasattr(input_data, 'read'):
            self._load_stream(input_data)
        elif hasattr(input_data, 'topil'):
            self._load_psd(input_data)
        else:
            self._load_storage(input_data)

    def _load_storage(self, url):
        storage = get_storage(os.path.dirname(url))
        filename = os.path.basename(url)
        with storage.open(filename) as f:
            self._load_stream(f)
        self._input = url

    def _load_stream(self, stream):
        self._input = None
        self._psd = PSDImage.open(stream)
        self._layer = self._psd

    def _load_psd(self, psd):
        self._input = None
        self._layer = psd
        while psd.parent is not None:
            psd = psd.parent
        self._psd = psd


class Writer:

    def _set_output(self, output_data):
        self.resource_path = 'files/'
        if self.resource_path is not None:
            self._resource = get_storage(os.path.join(os.path.dirname(output_data), self.resource_path), type='res')
        if not output_data:
            return
        if hasattr(output_data, 'write'):
            self._output = output_data
            return

        # save to a file.
        if not output_data.endswith('/') and os.path.isdir(output_data):
            output_data += '/'
        self._output = get_storage(os.path.dirname(output_data))
        self._output_file = os.path.basename(output_data)
        if not self._output_file:
            if hasattr(self, '_input'):
                basename = os.path.splitext(os.path.basename(self._input))[0]
                self._output_file = basename + '.html'

    def _save_html(self, content):
        # Write to the output.
        pretty_string = content
        if self._output_file:
            url = self._output.url(self._output_file)
            self._output.put(self._output_file, pretty_string.encode('utf-8'))
            return url
        if self._output:
            self._output.write(str(pretty_string))
            return self._output
        return pretty_string

    def _save_img(self, image, fmt='png', icc_profile=None):
        with io.BytesIO() as output:
            image.save(output, format=fmt, icc_profile=icc_profile)
            encoded_image = output.getvalue()
        if self._resource is not None:
            checksum = hashlib.md5(encoded_image).hexdigest()
            filename = checksum + '.' + fmt
            self._resource.put(filename, encoded_image)
            src = os.path.join(self.resource_path, filename)
        else:
            src = ('data:image/{};base64,'.format(fmt) + base64.b64encode(encoded_image).decode('utf-8'))

        return src
