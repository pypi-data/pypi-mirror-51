Simple use:
***********
.. code:: python

    >>> from Tools.common import Input
    >>> Input.GetInt()
    Please enter a number:2222
    It's Bigger, please re-enter:-1
    It's Smaller, please re-enter:22
    22
    >>> from Tools.Files import WordFile
    >>> wf = WordFile("E:/doc.docx")
    >>> print(wf.ToPDF("E:/pdf.pdf"))
    True
