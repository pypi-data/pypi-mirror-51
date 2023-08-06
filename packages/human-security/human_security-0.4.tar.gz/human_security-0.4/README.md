## Human Security

Basic security functions for human beings, and abstraction on top of cryptography

## Examples

```       
message = 'hello world'
h = HumanAES()
h.generate()
print 'secret key is', h.key
assert h.decrypt(h.encrypt(message)) == message
    
h = HumanRSA()
h.generate()
print h.public_pem()
print h.private_pem()
# h.load_private_pem(...)
# h.load_public_pem(...)
    
encrypted = h.encrypt(message)
decrypted = h.decrypt(encrypted)
assert decrypted == message
    
signature = h.sign(message)
assert h.verify(message, signature)
```

## License

BSD v3 - Created by Prof. Massimo Di Pierro, 2018

