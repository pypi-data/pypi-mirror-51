# crypto-commons

Small python module for common CTF crypto functions.
Feel free to contribute if you think there is something missing, or if you have some interesting code to share.

In general we want to keep this as much dependency-free as possible, so most likely pull requests with a lot of external dependencies will not get merged.

For the record: this is not a generic-purpose crypto library, nor production-level cryptography implementation!
You should not use any of this code in real-life applications.

The problems we want to solve here:

- The need to constantly look for implementations for some less common algorithms (like Damgard-Jurik) or less common scenarios (like RSA with prime powers).
- The need to install many different libraries in order to use some simple function.
- Issues with installing dependencies on different environments. 
Especially with Python 2/3 incompatibility and compiled C-modules.
- Repeating the same code over and over again, and wasting time on debugging typos and small mistakes.

General guidelines we hope to follow:
- Split implementation into small steps. CTF tasks often require changes in some of the algorithms, 
so it would be nice to be able to assemble an algorithm from smaller blocks. 
- Expose clear interfaces.
Object-oriented code might be nice for production-level software, 
but makes it more complicated when you're trying to translate primitives you have into objects the library requires.
Especially when you're missing some parameters, which are not necessary for the function you need.
- Don't make asserts and checks other than the necessary ones for current function.
Some libraries are not usable in CTF environment because they will automatically fail detecting some "invalid" parameters, 
while in reality we know the parameters are wrong and we need a few more steps to solve the task.

## Installation

``` bash
sudo python setup.py install
```
## Usage example

Basic usage:

``` python
from crypto_commons import generic

#xor a hex array with a string and print the result
a = [0x61, 0x53, 0x40, 0x47, 0x42, 0x59, 0x45, 0x5c, 0x08]
b = "123456789"

b = map(ord, b)

xored = map(chr, generic.xor(a, b))

print(''.join(xored))

```

[qiwi CTF, crypto 400](https://github.com/p4-team/ctf/blob/master/2016-11-17-qiwi-2016/hastad/README.md)

```python
from src.crypto_commons.generic import long_to_bytes
from src.crypto_commons.rsa.rsa_commons import hastad_broadcast


def main():
    n1 = 95118357989037539883272168746004652872958890562445814301889866663072352421703264985997800660075311645555799745426868343365321502734736006248007902409628540578635925559742217480797487130202747020211452620743021097565113059392504472785227154824117231077844444672393221838192941390309312484066647007469668558141
    n2 = 98364165919251246243846667323542318022804234833677924161175733253689581393607346667895298253718184273532268982060905629399628154981918712070241451494491161470827737146176316011843738943427121602324208773653180782732999422869439588198318422451697920640563880777385577064913983202033744281727004289781821019463
    n3 = 68827940939353189613090392226898155021742772897822438483545021944215812146809318686510375724064888705296373853398955093076663323001380047857809774866390083434272781362447147441422207967577323769812896038816586757242130224524828935043187315579523412439309138816335569845470021720847405857361000537204746060031
    c1 = 64830446708169012766414587327568812421130434817526089146190136796461298592071238930384707543318390292451118980302805512151790248989622269362958718228298427212630272525186478627299999847489018400624400671876697708952447638990802345587381905407236935494271436960764899006430941507608152322588169896193268212007
    c2 = 96907490717344346588432491603722312694208660334282964234487687654593984714144825656198180777872327279250667961465169799267405734431675111035362089729249995027326863099262522421206459400405230377631141132882997336829218810171728925087535674907455584557956801831447125486753515868079342148815961792481779375529
    c3 = 43683874913011746530056103145445250281307732634045437486524605104639785469050499171640521477036470750903341523336599602288176611160637522568868391237689241446392699321910723235061180826945464649780373301028139049288881578234840739545000338202917678008269794179100732341269448362920924719338148857398181962112
    print(long_to_bytes(hastad_broadcast([(c1, n1), (c2, n2), (c3, n3)])))


main()
```

[qiwi CTF again, crypto 400](https://github.com/p4-team/ctf/blob/master/2016-11-17-qiwi-2016/hensel/README.md)

```python
import gmpy2
from crypto_commons.generic import long_to_bytes
from crypto_commons.rsa.rsa_commons import hensel_lifting, modinv


def main():
    n = 158168890645747636339512652656727367370140893295030333823920833363025940906055891357316994482461476576118114207681214323912652527927215053128809927932495206979837034713724140745400652922252749994983891690894724877897453440237829719520264826887839607084620792280551479756249230842706713662875715392719130358089
    e = 65537
    c = 140823625180859595137593494178968497314300266616869468408596741823165198698204065579249727536890649445240801729293482339393915146972721826733382396566284303449925618355682242041225432010603850355326962069585919704623290128021782032477132287121179121257196031074006842188551083381364957799238533440938240326919
    p = gmpy2.isqrt(n)
    k = 2
    base = pow(c, modinv(e, p - 1), p)  # solution to pt^e mod p
    f = lambda x: pow(x, e, n) - c
    df = lambda x: e * x
    r = hensel_lifting(f, df, p, k, base)  # lift pt^e mod p to pt^e mod p^k
    for solution in r:
        print(long_to_bytes(solution))

main()

```
