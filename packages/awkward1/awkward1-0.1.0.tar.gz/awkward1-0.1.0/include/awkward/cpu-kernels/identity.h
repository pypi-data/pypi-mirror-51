// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARDCPU_IDENTITY_H_
#define AWKWARDCPU_IDENTITY_H_

#include "awkward/cpu-kernels/util.h"

extern "C" {
  Error awkward_identity_new(IndexType length, IndexType* to);
  Error awkward_identity_from_listfoffsets(IndexType length, IndexType width, IndexType* offsets, IndexType* from, IndexType tolength, IndexType* to);
}

#endif // AWKWARDCPU_IDENTITY_H_
