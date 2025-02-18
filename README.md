Handheld Wearable Keyboard with Binary Input
Inspiration
The idea for this project was inspired by the challenge of creating a compact and efficient text input system using minimal hardware. Traditional keyboards are bulky and not always practical for wearable or embedded applications. By implementing a 5-bit binary input system, we aimed to explore an alternative way of typing that is both lightweight and functional. This project was also an opportunity to deepen our understanding of binary encoding, input handling, and display interfacing.

What I Learned
Throughout this project, we gained hands-on experience in designing a simple but effective user interface using binary encoding. I learned how to efficiently capture and process user input from a limited number of buttons, implement a reliable character-mapping system, and display text dynamically on a small screen. Additionally, I improved my understanding of debouncing techniques to ensure accurate input detection and responsiveness.

How We Built It
The system consists of five push buttons, each representing a binary digit, and an additional button for confirming input (Enter). By pressing different combinations of the five buttons, users can encode letters, numbers, and symbols. The microcontroller processes the binary input, maps it to a corresponding character, and displays the output on a small screen.

For the display, we used an LCD screen to show the typed text in real-time. The firmware was written to handle input processing, debounce signals, and update the screen efficiently. A predefined lookup table converts binary values into readable characters, allowing users to input text seamlessly.

Challenges Faced
One major challenge was designing an intuitive and efficient way to enter characters using only five inputs. Since each letter or symbol requires a unique binary combination, optimizing the encoding system to minimize errors and improve typing speed was crucial. Additionally, handling mechanical switch debounce was necessary to prevent unintended inputs and ensure smooth operation. Another challenge was managing display updates efficiently to keep the text readable while maintaining real-time responsiveness.

Conclusion
This project successfully demonstrated an alternative text input method using binary encoding with minimal hardware. The compact design makes it suitable for wearable applications, and the experience provided valuable insights into efficient input handling and display interfacing. In the future, I plan to refine the encoding scheme, improve the user interface, and explore potential applications for accessibility and assistive technology.
