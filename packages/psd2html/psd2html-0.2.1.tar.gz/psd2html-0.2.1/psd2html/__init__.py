from psd2html.builder import Html
from psd2html.converter import LayerConvert
from psd2html.io import Reader, Writer


def psd2html(psd_file, html_file=None):
    psd = PSD2HTML()
    return psd.convert(psd_file, html_file)


class PSD2HTML(Reader, Writer, LayerConvert):

    def convert(self, psd, output=None):
        self._reset()
        self._set_input(psd)
        self._set_output(output)

        layer = self._layer
        elements = self.convert_layer(layer)
        html = Html()
        html.append(elements)

        return self._save_html(html.__str__())
