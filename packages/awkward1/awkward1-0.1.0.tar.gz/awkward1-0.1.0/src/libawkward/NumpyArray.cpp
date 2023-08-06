// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include "awkward/cpu-kernels/identity.h"
#include "awkward/NumpyArray.h"

using namespace awkward;

ssize_t NumpyArray::ndim() const {
  return shape_.size();
}

bool NumpyArray::isscalar() const {
  return ndim() == 0;
}

bool NumpyArray::isempty() const {
  for (auto x : shape_) {
    if (x == 0) return true;
  }
  return false;  // false for isscalar(), too
}

bool NumpyArray::iscompact() const {
  ssize_t x = itemsize_;
  for (ssize_t i = ndim() - 1;  i >= 0;  i--) {
    if (x != strides_[i]) return false;
    x *= shape_[i];
  }
  return true;  // true for isscalar(), too
}

void* NumpyArray::byteptr() const {
  return reinterpret_cast<void*>(reinterpret_cast<ssize_t>(ptr_.get()) + byteoffset_);
}

ssize_t NumpyArray::bytelength() const {
  if (isscalar()) {
    return itemsize_;
  }
  else {
    return shape_[0]*strides_[0];
  }
}

byte NumpyArray::getbyte(ssize_t at) const {
  return *reinterpret_cast<byte*>(reinterpret_cast<ssize_t>(ptr_.get()) + byteoffset_ + at);
}

void NumpyArray::setid(const std::shared_ptr<Identity> id) {
  id_ = id;
}

void NumpyArray::setid() {
  assert(!isscalar());
  std::shared_ptr<Identity> newid(new Identity(Identity::newref(), FieldLocation(), 0, 1, length()));
  Error err = awkward_identity_new(length(), newid.get()->ptr().get());
  HANDLE_ERROR(err);
  setid(newid);
}

const std::string NumpyArray::repr(const std::string indent, const std::string pre, const std::string post) const {
  std::stringstream out;
  out << indent << pre << "<NumpyArray format=\"" << format_ << "\" shape=\"";
  for (ssize_t i = 0;  i < ndim();  i++) {
    if (i != 0) {
      out << " ";
    }
    out << shape_[i];
  }
  out << "\" ";
  if (!iscompact()) {
    out << "strides=\"";
    for (ssize_t i = 0;  i < ndim();  i++) {
      if (i != 0) {
        out << ", ";
      }
      out << strides_[i];
    }
    out << "\" ";
  }
  out << "data=\"" << std::hex << std::setw(2) << std::setfill('0');
  ssize_t len = bytelength();
  if (len <= 32) {
    for (ssize_t i = 0;  i < len;  i++) {
      if (i != 0  &&  i % 4 == 0) {
        out << " ";
      }
      out << int(getbyte(i));
    }
  }
  else {
    for (ssize_t i = 0;  i < 16;  i++) {
      if (i != 0  &&  i % 4 == 0) {
        out << " ";
      }
      out << int(getbyte(i));
    }
    out << " ... ";
    for (ssize_t i = len - 16;  i < len;  i++) {
      if (i != len - 16  &&  i % 4 == 0) {
        out << " ";
      }
      out << int(getbyte(i));
    }
  }
  out << "\" at=\"0x";
  out << std::hex << std::setw(12) << std::setfill('0') << reinterpret_cast<ssize_t>(ptr_.get());
  if (id_.get() == nullptr) {
    out << "\"/>" << post;
  }
  else {
    out << "\">\n";
    out << id_.get()->repr(indent + std::string("    "), "", "\n");
    out << indent << "</NumpyArray>" << post;
  }
  return out.str();
}

IndexType NumpyArray::length() const {
  if (isscalar()) {
    return -1;
  }
  else {
    return (IndexType)shape_[0];
  }
}

std::shared_ptr<Content> NumpyArray::shallow_copy() const {
  return std::shared_ptr<Content>(new NumpyArray(id_, ptr_, shape_, strides_, byteoffset_, itemsize_, format_));
}

std::shared_ptr<Content> NumpyArray::get(IndexType at) const {
  assert(!isscalar());
  ssize_t byteoffset = byteoffset_ + strides_[0]*((ssize_t)at);
  const std::vector<ssize_t> shape(shape_.begin() + 1, shape_.end());
  const std::vector<ssize_t> strides(strides_.begin() + 1, strides_.end());
  std::shared_ptr<Identity> id;
  if (id_.get() != nullptr) {
    id = id_.get()->slice(at, at + 1);
  }
  return std::shared_ptr<Content>(new NumpyArray(id, ptr_, shape, strides, byteoffset, itemsize_, format_));
}

std::shared_ptr<Content> NumpyArray::slice(IndexType start, IndexType stop) const {
  assert(!isscalar());
  ssize_t byteoffset = byteoffset_ + strides_[0]*((ssize_t)start);
  std::vector<ssize_t> shape;
  shape.push_back((ssize_t)(stop - start));
  shape.insert(shape.end(), shape_.begin() + 1, shape_.end());
  std::shared_ptr<Identity> id;
  if (id_.get() != nullptr) {
    id = id_.get()->slice(start, stop);
  }
  return std::shared_ptr<Content>(new NumpyArray(id, ptr_, shape, strides_, byteoffset, itemsize_, format_));
}
