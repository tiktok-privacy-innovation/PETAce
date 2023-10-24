# PETAce

Privacy-Enhancing Technologies via Applied Cryptography Engineering (PETAce) enables fast prototyping of ideas based on privacy-enhancing technologies.
PETAce is a long-term development project and is planned to catch up with state-of-the-art research results in future releases.
It is implemented in C++ and is modularized into the following repositories.

- [PETAce-Solo](https://github.com/tiktok-privacy-innovation/PETAce-Solo) implements primitive hashing, encryption, and randomness generation algorithms performed by one party.
    - Hash functions: SHA-256, SHA3-256, and BLAKE2b
    - Psuedo-random number generators based on: SHAKE_128, BLAKE2Xb, and AES_ECB_CTR.
    - Sampling of bytes, 32-bit unsigned integers, and 64-bit unsigned integers from the uniform distribution
    - Prime field elliptic curve group arithmetics including hash-to-curve
    - Hashing tables: Cuckoo hashing and simple hashing
    - Partially homomorphic encryption: the Paillier cryptosystem
- [PETAce-Verse](https://github.com/tiktok-privacy-innovation/PETAce-Verse) includes frequently used cryptographic subprotocols such as oblivious transfer and oblivious shuffling.
    - [Naor-Pinkas OT](https://dl.acm.org/doi/10.5555/365411.365502)
    - [IKNP OT](https://link.springer.com/chapter/10.1007/978-3-540-45146-4_9) with [optimization](https://link.springer.com/article/10.1007/s00145-016-9236-6)
    - [KKRT OT](https://dl.acm.org/doi/abs/10.1145/2976749.2978381)
- [PETAce-Duet](https://github.com/tiktok-privacy-innovation/PETAce-Duet) abstracts general-purpose two-party secure computing operator protocols.
    - Protocols from [ABY](https://www.ndss-symposium.org/wp-content/uploads/2017/09/08_2_1.pdf)
    - Secure comparison protocols from [Cheetah](https://www.usenix.org/system/files/sec22-huang-zhicong.pdf)
    - The secure random shuffling protocol from [Secret-Shared Shuffle](https://link.springer.com/chapter/10.1007/978-3-030-64840-4_12)
    - Protocols that convert arithmetic shares to and from ciphertexts of the Paillier cryptosystem
    - Python API
- [PETAce-SetOps](https://github.com/tiktok-privacy-innovation/PETAce-SetOps) archives several protocols that perform private set operations.
    - An ECDH-PSI protocol based on Elliptic-Curve Diffie-Hellman
    - The [KKRT-PSI](https://dl.acm.org/doi/abs/10.1145/2976749.2978381) protocol based on Oblivious Pseudorandom Functions (OPRF)
    - A private join and compute protocol based on [Circuit-PSI](https://www.researchgate.net/publication/356421123_Circuit-PSI_With_Linear_Complexity_via_Relaxed_Batch_OPPRF)
- [PETAce-Network](https://github.com/tiktok-privacy-innovation/PETAce-Network) provides a preliminary interface of network communication.
    - Network abstract interface
    - Socket network implementation

## Contribution

Please check [Contributing](CONTRIBUTING.md) for more details.

## Code of Conduct

Please check [Code of Conduct](CODE_OF_CONDUCT.md) for more details.

## License

This project is licensed under the [Apache-2.0 License](LICENSE).

## Citing PETAce

To cite PETAce in academic papers, please use the following BibTeX entries.

### Version 0.2.0

```tex
    @misc{petace,
        title = {PETAce (release 0.2.0)},
        howpublished = {\url{https://github.com/tiktok-privacy-innovation/PETAce}},
        month = Oct,
        year = 2023,
        note = {TikTok Pte. Ltd.},
        key = {PETAce}
    }
```
