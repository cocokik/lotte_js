Option Explicit
Private Declare PtrSafe Function CallNextHookEx Lib "user32" (ByVal hHook As LongPtr, _
    ByVal ncode As LongPtr, ByVal wParam As LongPtr, lParam As Any) As LongPtr

Private Declare PtrSafe Function GetModuleHandle Lib "kernel32" Alias "GetModuleHandleA" (ByVal lpModuleName As String) As LongPtr

Private Declare PtrSafe Function SetWindowsHookEx Lib "user32" Alias "SetWindowsHookExA" _
    (ByVal idHook As LongPtr, ByVal lpfn As LongPtr, ByVal hmod As LongPtr, ByVal dwThreadId As LongPtr) As LongPtr

Private Declare PtrSafe Function UnhookWindowsHookEx Lib "user32" (ByVal hHook As LongPtr) As LongPtr

Private Declare PtrSafe Function SendDlgItemMessage Lib "user32" Alias "SendDlgItemMessageA" _
(ByVal hDlg As LongPtr, ByVal nIDDlgItem As LongPtr, ByVal wMsg As LongPtr, ByVal wParam As LongPtr, ByVal lParam As LongPtr) As LongPtr

Private Declare PtrSafe Function GetClassName Lib "user32" Alias "GetClassNameA" (ByVal hwnd As LongPtr, _
ByVal lpClassName As String, ByVal nMaxCount As LongPtr) As LongPtr

Private Declare PtrSafe Function GetCurrentThreadId Lib "kernel32" () As LongPtr

Private Const EM_SETPASSWORDCHAR = &HCC
Private Const WH_CBT = 5
Private Const HCBT_ACTIVATE = 5
Private Const HC_ACTION = 0

Private hHook As LongPtr


Public Function NewProc(ByVal lngCode As LongPtr, ByVal wParam As LongPtr, ByVal lParam As LongPtr) As LongPtr
    Dim RetVal
    Dim strClassName As String, lngBuffer As LongPtr

    If lngCode < HC_ACTION Then
        NewProc = CallNextHookEx(hHook, lngCode, wParam, lParam)
        Exit Function
    End If

    strClassName = String$(256, " ")
    lngBuffer = 255

    If lngCode = HCBT_ACTIVATE Then
        RetVal = GetClassName(wParam, strClassName, lngBuffer)
        If Left$(strClassName, RetVal) = "#32770" Then
            SendDlgItemMessage wParam, &H1324, EM_SETPASSWORDCHAR, Asc("*"), &H0
        End If
    End If

    CallNextHookEx hHook, lngCode, wParam, lParam
End Function

Public Function PasswordBox(Prompt, Title) As String
    Dim lngModHwnd As LongPtr, lngThreadID As LongPtr

    lngThreadID = GetCurrentThreadId
    lngModHwnd = GetModuleHandle(vbNullString)

    hHook = SetWindowsHookEx(WH_CBT, AddressOf NewProc, lngModHwnd, lngThreadID)

    PasswordBox = InputBox(Prompt, Title)
    UnhookWindowsHookEx hHook
End Function

