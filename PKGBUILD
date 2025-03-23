# PKGBUILD
pkgname=dotts
pkgver=1.0.0
pkgrel=1
pkgdesc="The Dotfiles Manager from the Future"
arch=('any')
url="https://github.com/yourusername/dotts"
license=('MIT')
depends=('python' 'python-pip')
source=("$pkgname-$pkgver.tar.gz::https://github.com/yourusername/dotts/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Replace with the actual checksum after building

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py install --root="$pkgdir"
}
