# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 23:22:11 2022

@author: me
"""

import ddddocr

ocr = ddddocr.DdddOcr()
with open('./response.png', 'rb') as f :
     img_bytes = f.read()

res = ocr.classification(img_bytes)
print("\n"+res)