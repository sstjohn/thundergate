/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015-2026  Saul St. John
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

//
// tgctl -- the container application for the ThunderGate dext.
//
// A driver extension can only be installed by an application bundle that
// embeds it. tgctl is that bundle: it submits an OSSystemExtensionRequest
// to activate (or deactivate) the embedded TGDext, reports progress, and
// exits. The actual device work is done by py/ talking to the dext over
// IOKit (see py/interfaces/macos.py).
//
// Usage:
//   tgctl              activate the dext
//   tgctl deactivate   deactivate the dext
//

import Foundation
import SystemExtensions

let dextIdentifier = "lol.ssj.thundergate.TGDext"

final class RequestDelegate: NSObject, OSSystemExtensionRequestDelegate {

    func request(_ request: OSSystemExtensionRequest,
                 actionForReplacingExtension existing: OSSystemExtensionProperties,
                 withExtension ext: OSSystemExtensionProperties)
            -> OSSystemExtensionRequest.ReplacementAction {
        print("tgctl: replacing installed dext "
              + "\(existing.bundleShortVersion) (\(existing.bundleVersion)) "
              + "with \(ext.bundleShortVersion) (\(ext.bundleVersion))")
        return .replace
    }

    func requestNeedsUserApproval(_ request: OSSystemExtensionRequest) {
        print("tgctl: awaiting approval -- open System Settings > General > "
              + "Login Items & Extensions and allow the extension, then "
              + "re-run if necessary.")
    }

    func request(_ request: OSSystemExtensionRequest,
                 didFinishWithResult result: OSSystemExtensionRequest.Result) {
        switch result {
        case .completed:
            print("tgctl: done -- dext active.")
        case .willCompleteAfterReboot:
            print("tgctl: done -- dext will be active after a reboot.")
        @unknown default:
            print("tgctl: done -- result \(result.rawValue).")
        }
        exit(0)
    }

    func request(_ request: OSSystemExtensionRequest,
                 didFailWithError error: Error) {
        FileHandle.standardError.write(
            Data("tgctl: request failed: \(error.localizedDescription)\n".utf8))
        exit(1)
    }
}

let delegate = RequestDelegate()

let deactivate = CommandLine.arguments.dropFirst().contains("deactivate")
let request: OSSystemExtensionRequest = deactivate
    ? .deactivationRequest(forExtensionWithIdentifier: dextIdentifier,
                           queue: .main)
    : .activationRequest(forExtensionWithIdentifier: dextIdentifier,
                         queue: .main)
request.delegate = delegate

print("tgctl: submitting \(deactivate ? "deactivation" : "activation") "
      + "request for \(dextIdentifier)")
OSSystemExtensionManager.shared.submitRequest(request)

RunLoop.main.run()
