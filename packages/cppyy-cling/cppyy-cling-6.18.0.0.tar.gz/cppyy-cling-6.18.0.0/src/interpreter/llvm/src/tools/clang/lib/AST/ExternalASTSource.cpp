//===- ExternalASTSource.cpp - Abstract External AST Interface --*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
//  This file provides the default implementation of the ExternalASTSource 
//  interface, which enables construction of AST nodes from some external
//  source.
//
//===----------------------------------------------------------------------===//

#include "clang/AST/ExternalASTSource.h"
#include "clang/AST/ASTContext.h"
#include "clang/AST/DeclarationName.h"
#include "clang/Basic/Module.h"
#include "llvm/Support/ErrorHandling.h"

using namespace clang;

ExternalASTSource::~ExternalASTSource() { }

uint32_t ExternalASTSource::getGeneration(const ASTContext &C) const {
  return C.getGeneration();
}

llvm::Optional<ExternalASTSource::ASTSourceDescriptor>
ExternalASTSource::getSourceDescriptor(unsigned ID) {
  return None;
}

ExternalASTSource::ExtKind
ExternalASTSource::hasExternalDefinitions(const Decl *D) {
  return EK_ReplyHazy;
}

ExternalASTSource::ASTSourceDescriptor::ASTSourceDescriptor(const Module &M)
  : Signature(M.Signature), ClangModule(&M) {
  if (M.Directory)
    Path = M.Directory->getName();
  if (auto *File = M.getASTFile())
    ASTFile = File->getName();
}

std::string ExternalASTSource::ASTSourceDescriptor::getModuleName() const {
  if (ClangModule)
    return ClangModule->Name;
  else
    return PCHModuleName;
}

void ExternalASTSource::FindFileRegionDecls(FileID File, unsigned Offset,
                                            unsigned Length,
                                            SmallVectorImpl<Decl *> &Decls) {}

void ExternalASTSource::CompleteRedeclChain(const Decl *D) {}

void ExternalASTSource::CompleteType(TagDecl *Tag) {}

void ExternalASTSource::CompleteType(ObjCInterfaceDecl *Class) {}

void ExternalASTSource::ReadComments() {}

void ExternalASTSource::StartedDeserializing() {}

void ExternalASTSource::FinishedDeserializing() {}

void ExternalASTSource::StartTranslationUnit(ASTConsumer *Consumer) {}

void ExternalASTSource::PrintStats() { }

bool ExternalASTSource::layoutRecordType(
    const RecordDecl *Record, uint64_t &Size, uint64_t &Alignment,
    llvm::DenseMap<const FieldDecl *, uint64_t> &FieldOffsets,
    llvm::DenseMap<const CXXRecordDecl *, CharUnits> &BaseOffsets,
    llvm::DenseMap<const CXXRecordDecl *, CharUnits> &VirtualBaseOffsets) {
  return false;
}

Decl *ExternalASTSource::GetExternalDecl(uint32_t ID) {
  return nullptr;
}

Selector ExternalASTSource::GetExternalSelector(uint32_t ID) {
  return Selector();
}

uint32_t ExternalASTSource::GetNumExternalSelectors() {
   return 0;
}

Stmt *ExternalASTSource::GetExternalDeclStmt(uint64_t Offset) {
  return nullptr;
}

CXXCtorInitializer **
ExternalASTSource::GetExternalCXXCtorInitializers(uint64_t Offset) {
  return nullptr;
}

CXXBaseSpecifier *
ExternalASTSource::GetExternalCXXBaseSpecifiers(uint64_t Offset) {
  return nullptr;
}

bool
ExternalASTSource::FindExternalVisibleDeclsByName(const DeclContext *DC,
                                                  DeclarationName Name) {
  return false;
}

void ExternalASTSource::completeVisibleDeclsMap(const DeclContext *DC) {}

void ExternalASTSource::FindExternalLexicalDecls(
    const DeclContext *DC, llvm::function_ref<bool(Decl::Kind)> IsKindWeWant,
    SmallVectorImpl<Decl *> &Result) {}

void ExternalASTSource::getMemoryBufferSizes(MemoryBufferSizes &sizes) const {}

uint32_t ExternalASTSource::incrementGeneration(ASTContext &C) {
  return C.incrementGeneration();
}
