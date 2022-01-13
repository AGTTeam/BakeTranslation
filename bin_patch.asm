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

  VERTICAL_TEXT:
  lw a0,0x30(s1)
  sra a0,a0,0x6
  j VERTICAL_TEXT_RET
  move a1,a0

  CONVERT_VERTICAL:
  move s1,a1
  ;Check if we're drawing vertical text
  lw a1,0x24(a2)
  bne a1,0x1,@@ret
  andi a0,a0,0xffff
  ;Return if the character is > 0x7e
  bgt a0,0x7e,@@ret
  nop
  ;Return an hardcoded value for the space
  beql a0,0x20,@@ret
  li a0,0x3005
  ;Add 0x3020 to the character code and tweak it for charcode gaps
  blt a0,0x70,@@done
  addiu a1,a0,0x3020
  blt a0,0x72,@@done
  addiu a1,a1,2
  addiu a1,a1,13
  @@done:
  move a0,a1
  @@ret:
  move s6,a0
  j CONVERT_VERTICAL_RET
  move a1,s1

  ;A copy of the function at 0x088ae390 to return a short character name
  GET_SHORT_CHAR_NAME3:
  addiu sp,sp,-0x10
  sw ra,0x0(sp)
  jal GET_SHORT_CHAR_NAME2
  lw a0,0x50B8(a0)
  lw a0,0x0897f380
  jal 0x088b58d8
  move a1,v0
  lw ra,0x0(sp)
  jr ra
  addiu sp,sp,0x10

  ;A copy of the function at 0x08833bf8 to return a short character name
  GET_SHORT_CHAR_NAME2:
  addiu sp,sp,-0x10
  lui a1,0x898
  sw s0,0x0(sp)
  sw ra,0x4(sp)
  jal GET_SHORT_CHAR_NAME
  lw s0,-0x70a0(a1)
  move a0,s0
  li a1,0
  jal 0x0880a504
  move a2,v0
  lw s0,0x0(sp)
  lw ra,0x4(sp)
  jr ra
  addiu sp,sp,0x10

  ;Return short character name ID
  GET_SHORT_CHAR_NAME:
  sltiu a1,a0,0xc
  beq a1,zero,GET_SHORT_CHAR_NAME_RET
  nop
  addiu v0,a0,0x5b
  GET_SHORT_CHAR_NAME_RET:
  jr ra
  nop

  ;Wrap the sprintf function by repeating the parameter
  SPRINTF_REPEAT:
  addiu sp,sp,-0x10
  sw ra,0x0(sp)
  jal 0x088cf7f8
  move a3,a2
  lw ra,0x0(sp)
  jr ra
  addiu sp,sp,0x10
  .endarea

;Handle vertical text VWF
.org 0x088e4da8
  j VERTICAL_TEXT
  sw zero,0x2c(s1)
  nop
  nop
  nop
  VERTICAL_TEXT_RET:

;Convert the character code for vertical text
.org 0x088e49ec
  j CONVERT_VERTICAL
  move s0,a1
  CONVERT_VERTICAL_RET:

;This function has a list of harcoded characters that are offset
;when rendering them vertically, we just don't care about this
.org 0x088266bc
  jr ra
  li v0,0x0

;Swap date order for save games
.org 0x088094a0
  lhu a2,0x212(sp) ;MM
  lhu a3,0x214(sp) ;DD
  lhu t0,0x210(sp) ;YYYY

;Swap order for "%sで対%s語録が|使えるようになりました。||対%s戦オススメの語録で|シングルモードでのみ使用可能な語録です。"
.org 0x088cd2d4
  move a2,s1
  move a3,s3

;Add more space for the "Glossary n" lines
.org 0x0881da9c
  addiu s4,s4,0x12

;Use short character names in the menu
;Original:
;4F: 阿良々木暦
;50: 戦場ヶ原ひたぎ
;51: 八九寺真宵
;54: 神原駿河
;52: 千石撫子
;53: 羽川翼
;55: ブラック羽川
;59: 阿良々木火憐
;5A: 阿良々木月火
;56: 忍野メメ
;57: 忍野忍
.macro short_char_names
  .dw 0x5b ;暦
  .dw 0x5c ;ひたぎ
  .dw 0x5d ;真宵
  .dw 0x60 ;駿河
  .dw 0x5e ;撫子
  .dw 0x5f ;翼
  .dw 0x61 ;猫
  .dw 0x65 ;火憐
  .dw 0x66 ;月火
  .dw 0x62 ;メメ
  .dw 0x63 ;忍
.endmacro
.org 0x0897c728
  short_char_names
.org 0x0897dd7c
  short_char_names

;Use short character names in menu headers
.org 0x088af798
  jal GET_SHORT_CHAR_NAME3 - 0x8804000

;Repeat sprintf parameter for these two strings:
;"%sの「中敵」語録が開放されました。|フリー対戦モード限定のＣＯＭ専用語録です。|より強力なＣＯＭと会話劇ができます。"
.org 0x088cd1e4
  jal SPRINTF_REPEAT - 0x8804000
;"%sの「強敵」語録が開放されました。|フリー対戦モード限定のＣＯＭ専用語録です。|最強難易度に挑戦してみてください！"
.org 0x088cd214
  jal SPRINTF_REPEAT - 0x8804000

;Align "Achievements" header
.org 0x088bc20c
  ;lui v0,0x41a0
  lui v0,0x4140

;Don't use installed data, always return 0 from the function that checks for it
.org 0x08807438
  j 0x08807470
  nop
;Do not prompt to install data on new game
.org 0x088232c4
  ;li a1,0xa
  li a1,0xb

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
