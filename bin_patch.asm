.psp
.open "BakeData/repack/PSP_GAME/SYSDIR/BOOT.BIN",0x8803F40

;Freed space until 0x0896863c
.org 0x08968278
  .area 0x3c3
  SWAP_CIRCLE_CROSS:
  move t0,a1
  lbu a1,0x5(t0)
  srl a2,a1,5
  srl a3,a1,6
  xor a2,a2,a3
  andi a2,a2,0x1
  sll a3,a2,5
  sll a2,a2,6
  or a2,a2,a3
  xor a2,a1,a2
  sb a2,0x5(t0)
  move a1,t0
  ;Original code
  lw s1,0x4(a1)
  lw a2,0x0(a0)
  j SWAP_CIRCLE_CROSS_RET
  nop

  SCE_SAVE:
  li a2,0x1
  sw a2,0x4(a1)
  sw a2,0x8(a1)
  j SCE_SAVE_RET
  li a2,0x13
  .endarea

;Set the language to 1 (English) and buttonSwap to 1 (X) for syscalls
;sceImposeSetLanguageMode
.org 0x0880706c
  li a1,0x1
  .skip 8
  li a0,0x1
;sceUtilitySavedataInitStart
.org 0x08807174
  j SCE_SAVE
  .skip 4
  SCE_SAVE_RET:

;Swap Circle with Cross
;Call the code after the sceCtrlReadBufferPositive call
.org 0x088ebd28
  j SWAP_CIRCLE_CROSS
  nop
  SWAP_CIRCLE_CROSS_RET:

;Redirect some error codes to free up some space
ERROR_PTR equ 0x08968250 - 0x08804000
.org 0x08925d24
  lui a1,hi(ERROR_PTR)
  addiu a1,a1,lo(ERROR_PTR)
.org 0x08926184
  li a1,ERROR_PTR
.org 0x0892619c
  addiu a1,a1,lo(ERROR_PTR)
.org 0x089261c8
  addiu a1,a1,lo(ERROR_PTR)
.org 0x089261ec
  addiu a1,a1,lo(ERROR_PTR)
.org 0x08926450
  lui a1,hi(ERROR_PTR)
  .skip 4
  addiu a1,a1,lo(ERROR_PTR)
.org 0x089264d8
  lui a1,hi(ERROR_PTR)
  .skip 4
  addiu a1,a1,lo(ERROR_PTR)
.org 0x089264e4
  lui a1,hi(ERROR_PTR)
  .skip 8
  addiu a1,a1,lo(ERROR_PTR)
.org 0x089264f8
  lui a1,hi(ERROR_PTR)
  .skip 4
  addiu a1,a1,lo(ERROR_PTR)
.org 0x08926504
  lui a1,hi(ERROR_PTR)
  .skip 4
  addiu a1,a1,lo(ERROR_PTR)
.org 0x08926698
  lui a1,hi(ERROR_PTR)
  .skip 4
  addiu a1,a1,lo(ERROR_PTR)
.close
