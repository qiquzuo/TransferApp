"""
生成自签名SSL证书
用于HTTPS加密传输
"""
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
import os

def generate_self_signed_cert(cert_file="cert.pem", key_file="key.pem", days=365):
    """生成自签名SSL证书"""
    
    print("🔐 正在生成SSL证书...")
    
    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # 获取本机IP作为Common Name
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = 'localhost'
    
    # 生成证书
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Beijing"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Beijing"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "TransferApp"),
        x509.NameAttribute(NameOID.COMMON_NAME, local_ip),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=days)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(local_ip)]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # 保存证书
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # 保存私钥
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print(f"✅ 证书生成成功！")
    print(f"📄 证书文件: {os.path.abspath(cert_file)}")
    print(f"🔑 私钥文件: {os.path.abspath(key_file)}")
    print(f"🌐 服务器IP: {local_ip}")
    print(f"⏰ 有效期: {days}天")
    print("\n💡 提示：首次访问时浏览器会显示安全警告，点击'继续访问'即可")
    
    return cert_file, key_file

if __name__ == "__main__":
    generate_self_signed_cert()
