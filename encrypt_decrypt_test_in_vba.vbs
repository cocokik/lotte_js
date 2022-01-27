
Option Explicit

Public Const INITIALIZATION_VECTOR = "dlrs$5kd"  'Always 8 characters

Public Const TRIPLE_DES_KEY = ">aaa8adk=35K{dsa" 'Always 16 characters





Sub TestEncrypt()
    MsgBox "This is an encrypted string: -> " & EncryptStringTripleDES("wltjd123###@@!!")
    Debug.Print EncryptStringTripleDES("This is an encrypted string:")
End Sub

Sub TestDecrypt()
    MsgBox "u99CVItCGiMQEVYHf8+S22QbJ5CPQGDXuS5n1jvEIgU= -> " & DecryptStringTripleDES("NETUvSt3IqpGVqigkg5kXw==")
End Sub


Function EncryptStringTripleDES(plain_string As String) As Variant

    Dim encryption_object As Object
    Dim plain_byte_data() As Byte
    Dim encrypted_byte_data() As Byte
    Dim encrypted_base64_string As String

    EncryptStringTripleDES = Null

    On Error GoTo FunctionError

    plain_byte_data = CreateObject("System.Text.UTF8Encoding").GetBytes_4(plain_string)

    Set encryption_object = CreateObject("System.Security.Cryptography.TripleDESCryptoServiceProvider")
    encryption_object.Padding = 3
    encryption_object.Key = CreateObject("System.Text.UTF8Encoding").GetBytes_4(TRIPLE_DES_KEY)
    encryption_object.IV = CreateObject("System.Text.UTF8Encoding").GetBytes_4(INITIALIZATION_VECTOR)
    encrypted_byte_data = _
            encryption_object.CreateEncryptor().TransformFinalBlock(plain_byte_data, 0, UBound(plain_byte_data) + 1)

    encrypted_base64_string = BytesToBase64(encrypted_byte_data)

    EncryptStringTripleDES = encrypted_base64_string

    Exit Function

FunctionError:

    MsgBox "TripleDES encryption failed"

End Function

Function DecryptStringTripleDES(encrypted_string As String) As Variant

    Dim encryption_object As Object
    Dim encrypted_byte_data() As Byte
    Dim plain_byte_data() As Byte
    Dim plain_string As String

    DecryptStringTripleDES = Null

    On Error GoTo FunctionError

    encrypted_byte_data = Base64toBytes(encrypted_string)

    Set encryption_object = CreateObject("System.Security.Cryptography.TripleDESCryptoServiceProvider")
    encryption_object.Padding = 3
    encryption_object.Key = CreateObject("System.Text.UTF8Encoding").GetBytes_4(TRIPLE_DES_KEY)
    encryption_object.IV = CreateObject("System.Text.UTF8Encoding").GetBytes_4(INITIALIZATION_VECTOR)
    plain_byte_data = encryption_object.CreateDecryptor().TransformFinalBlock(encrypted_byte_data, 0, UBound(encrypted_byte_data) + 1)

    plain_string = CreateObject("System.Text.UTF8Encoding").GetString(plain_byte_data)

    DecryptStringTripleDES = plain_string

    Exit Function

FunctionError:

    MsgBox "TripleDES decryption failed"

End Function


Function BytesToBase64(varBytes() As Byte) As String
    With CreateObject("MSXML2.DomDocument").createElement("b64")
        .DataType = "bin.base64"
        .nodeTypedValue = varBytes
        BytesToBase64 = Replace(.Text, vbLf, "")
    End With
End Function


Function Base64toBytes(varStr As String) As Byte()
    With CreateObject("MSXML2.DOMDocument").createElement("b64")
         .DataType = "bin.base64"
         .Text = varStr
         Base64toBytes = .nodeTypedValue
    End With
End Function



