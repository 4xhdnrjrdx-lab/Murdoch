import Foundation
import Vision
let file = CommandLine.arguments[1]
let detect = VNDetectBarcodesRequest()
detect.symbologies = [.qr]
detect.usesCPUOnly = true
try VNImageRequestHandler(url:URL(fileURLWithPath:file),options:[:]).perform([detect])
let result = detect.results?.compactMap{$0.payloadStringValue} ?? []
print(result)
assert(result.contains("https://cedar-retail-adkar-demo.spicy-rhino-0802.chatgpt.site/"))
