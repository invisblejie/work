class VigenereAutokeyCipher:
    def __init__(self, key, abc):
        self.key = key
        self.abc = abc

    def encode(self, text):
        '''When it need to encode a letter, the cipher always be ChangeKey[0]'''
        ChangeKey = self.key
        Encode = ''
        for i in text:
            if self.abc.find(i) == -1:
                Encode += i
            else: 
                Shift = self.abc.find(ChangeKey[0])
                Encode += self.abc[(self.abc.find(i) + Shift) % (len(self.abc))] 
                ChangeKey = ChangeKey[1:] + i 
        return Encode

    def decode(self, text):
        '''When it need to decode a letter, the cipher always be ChangeKey[0]'''
        ChangeKey = self.key
        Decode = ''
        for j in text:
            if self.abc.find(j) == -1:
                Decode += j
            else: 
                Shift = self.abc.find(ChangeKey[0])
                Decode += self.abc[(self.abc.find(j) - Shift + len(self.abc)) % (len(self.abc))] 
                ChangeKey = ChangeKey[1:] + Decode[-1]
        return Decode
        
                        
key = u'\u3072\u3089\u304b\u306a'
abc = u'\u3042\u3044\u3046\u3048\u304a\u3041\u3043\u3045\u3047\u3049\u304b\u304d\u304f\u3051\u3053\u3055\u3057\u3059\u305b\u305d\u305f\u3061\u3064\u3063\u3066\u3068\u306a\u306b\u306c\u306d\u306e\u306f\u3072\u3075\u3078\u307b\u307e\u307f\u3080\u3081\u3082\u3084\u3083\u3086\u3085\u3088\
u3087\u3089\u308a\u308b\u308c\u308d\u308f\u3092\u3093\u30fc'


c = VigenereAutokeyCipher(key, abc)
##print(c.encode('AAAAAAAAPASSWORDAAAAAAAA'))
print(c.decode(u'\u3069\u3082\u3042\u307f\u304c\u3068\u3054\u3056\u3044\u307e\u306c'))

