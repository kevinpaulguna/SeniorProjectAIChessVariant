#  AI Playable Fuzzy Logic Chess Variants<br/>Senior Project Group 4B

This project implements 2 variants of Chess:
1. **Fuzzy Logic Medieval Chess**
   - builds on Fuzzy-Logic Chess to create game-play resembling a medieval battle, using the standard chess board.
   - Pieces have different battle capabilities like their historical counterparts: mounted and armored Knights and royalty (King, Queen), pikemen, infantry (Pawns, Bishops), and archers (Rooks).
   - A Capture Table shows how the different pieces fare in battle against each other.
   - Moving and capturing are separate actions, and *up to* three actions may be taken in each turn.
   - The game ends with the capture of a King.
2. **Corp Command Fuzzy Logic Medieval Chess**
   -  builds on Fuzzy Logic Medieval Chess to create game-play resembling a medieval battle, using the standard chess board, with real-world command and control considerations.
   - The "armies" of chess pieces for command are divided into three "corp", of which the King and two Bishops are the commanders.
   - Each corp has its own move, totalling 3 per turn. Additionally, each commander can make a non attcking, one spot move.
   - The King may delegate or recall pieces from the Bishops, who can only have a maximum of six pieces in their corps. There is only one delegation/recall move allowed per turn.
   - If captured, a Bishop's commanded pieces revert to the authority of the King, and the move(s) for that corp are no longer available i.e. there is one less move per turn.
   - The Bishops will not fight on without their King; the game ends with the capture of a King.

## Status:
- **Frontend**: Refinement 🟢
- **Backend**: Refinement 🟢
- **AI**: Developing 🟡

## Contributors:
- [**Abdullah**](https://github.com/AbdullahEhsan) (Backend, assisted with AI and Frontend)
- [**Ben**](https://github.com/bbeebe1) (Backend)
- [**Brian**](https://github.com/Bkim0316) (AI, assisted with Backend)
- [**Eric**](https://github.com/Ericphan7) (Frontend)
- [**Kevinpaul**](https://github.com/kevinpaulguna) (initially assigned to Frontend, now assigned to AI)
- [**Seth**](https://github.com/ExhaustedDev) (Frontend, Backend)
- [**Teddy**](https://github.com/ted4bartz) (AI)